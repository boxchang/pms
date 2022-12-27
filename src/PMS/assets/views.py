#!/usr/bin/python
# coding=utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from assets.forms import AssetModelForm, AssetSearchForm
from assets.models import Asset, AssetArea, AssetCategory, AssetStatus, AssetType, Brand, Label_attachment, Series, Location, Unit
import openpyxl
from django.http import JsonResponse
import os
from PMS.settings.base import ASSET_BTW_FILE, EXE_FILE, NON_ASSET_BTW_FILE, PRINTER, BASE_DIR
import csv
from datetime import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, Http404

def print_cmd(EXCEL_FILE, BTW_FILE):
    CMD = """{EXE_FILE} /AF=\"{BTW_FILE}\" /D=\"{EXCEL_FILE}\" /PRN=\"{PRINTER}\" /P/X""".format(EXE_FILE=EXE_FILE, BTW_FILE=BTW_FILE, EXCEL_FILE=EXCEL_FILE, PRINTER=PRINTER)
    print(CMD)
    os.system(CMD)

@login_required
def index(request):
    return render(request, 'assets/index.html', locals())

def get_main_url(request):
    return reverse('assets_main')

#刪除
def delete(request, pk):
    if request.method == "GET":
        asset = Asset.objects.get(id=pk)
        asset.delete()
        return redirect(get_main_url(request))
    return render(request, 'assets/main.html', locals())

#查詢
def search(request):
    assets = Asset.objects.all()
    if request.method == "POST":
        _asset_no = request.POST.get('asset_no')
        _status = request.POST.get('status')
        _category = request.POST.get('category')
        _type = request.POST.get('type')
        _area = request.POST.get('area')
        _location = request.POST.get('location')
        _scrap = request.POST.get('scrap')

        if _asset_no:
            assets = assets.filter(asset_no=_asset_no)

        if _status:
            assets = assets.filter(status=_status)

        if _category:
            assets = assets.filter(category=_category)

        if _type:
            assets = assets.filter(type=_type)

        if _area:
            assets = assets.filter(area=_area)

        if _location:
            assets = assets.filter(location=_location)

        if not _scrap:
            assets = assets.exclude(status=AssetStatus.objects.get(status_name="已報廢"))

    return render(request, 'assets/search.html', locals())

#新增
def create(request):
    if request.method == "POST":
        form = AssetModelForm(request.POST)
        if form.is_valid():
            _category = form.cleaned_data.get('category')
            _type = form.cleaned_data.get('type')
            _location = form.cleaned_data.get('location')
            _auto_encode = form.cleaned_data.get('auto_encode')

            tmp_form = form.save(commit=False)
            if _auto_encode:
                tmp_form.asset_no = get_series_number(_category, _type, _location)
            tmp_form.create_by = request.user
            tmp_form.update_by = request.user
            form.save()

            return redirect(tmp_form.get_absolute_url())
    else:
        form = AssetModelForm()

    return render(request, 'assets/edit.html', locals())

#修改
def update(request, pk):
    mode = "UPDATE"
    asset = Asset.objects.get(id=pk)
    if request.method == "POST":
        form = AssetModelForm(request.POST, instance=asset)
        if form.is_valid():
            tmp_form = form.save(commit=False)
            tmp_form.save()
            return redirect(tmp_form.get_absolute_url())
    else:
        form = AssetModelForm(instance=asset)

    return render(request, 'assets/edit.html', locals())

#滾序號
def get_series_number(asset_category, asset_type, asset_location):
    type_code = asset_type.type_code  # 縮寫
    type_name = asset_type.type_name.upper()
    asset_category_id = str(asset_category.id)
    asset_category_name = str(asset_category.category_name)
    asset_location_id = str(asset_location.id)
    asset_location_name = str(asset_location.location_name)
    asset_type_id = str(asset_type.id)
    asset_type_name = str(asset_type.type_name)

    _key = ""
    _key_name = ""
    if asset_category_id == "1":  # 資訊設備
        if type_name == "NOTEBOOK":
            series_code = "TWKHHN"
        elif type_name == "COMPUTER":
            series_code = "TWKHHD"
        elif type_name == "MOBILE":
            series_code = "TWKHHM"
        else:
            series_code = "IT-" + type_code + "-"
        _key = asset_category_id.zfill(3) + asset_type_id.zfill(3)
        _key_name = asset_category_name + "_" + asset_type_name
    elif asset_category_id == "2":  # 辦公設備
        loc_obj = Location.objects.filter(id=asset_location_id)
        location_code = loc_obj[0].location_code
        series_code = "A-" + location_code + "-" + type_code + "-"
        _key = asset_category_id.zfill(3) + asset_location_id.zfill(3) + asset_type_id.zfill(3)
        _key_name = asset_category_name + "_" + asset_location_name + "_" + asset_type_name

    # 滾序號
    obj = Series.objects.filter(key=_key)
    if obj:
        _series = obj[0].series + 1
        obj.update(series=_series, desc=_key_name)
    else:
        _series = 1
        series = Series.objects.create(key=_key, series=1)

    if asset_category_id == "1":  # 資訊設備
        if type_name == "NOTEBOOK" or type_name == "COMPUTER":
            series_format = str(_series).zfill(4)
        else:
            series_format = str(_series).zfill(5)
    elif asset_category_id == "2":  # 辦公設備
        series_format = str(_series).zfill(3)

    series_code = series_code + series_format

    return series_code

#明細
def detail(request, pk):
    try:
        asset = Asset.objects.get(pk=pk)
    except Asset.DoesNotExist:
        raise Http404('Book does not exist')


    return render(request, 'assets/detail.html', locals())

#回主頁
def main(request):
    form = AssetSearchForm()
    return render(request, 'assets/main.html', locals())

#刪除Label檔案
def delete_csv(file_name):
    try:
        os.remove(file_name)
    except OSError as e:
        print(e)
    else:
        print("File is deleted successfully")

#文字轉CSV
def TEXT2CSV(asset_number):
    now = datetime.now()
    file_name = datetime.strftime(now, '%Y%m%d %H%M%S') + ".csv"
    file_name = os.path.join(BASE_DIR, 'media', 'uploads', 'label', file_name)

    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = ['NUMBER']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'NUMBER': asset_number})
    return file_name

#印標籤專頁
def label(request):
    if request.method == 'POST':
        label_type = request.POST.get('label_type', False)

        if label_type == 'single_asset_label':
            asset_label = request.POST.get('asset_number', False)
            csv = TEXT2CSV(asset_label)
            print_cmd(csv, ASSET_BTW_FILE)
            delete_csv(csv)

        elif label_type == 'single_nonasset_label':
            asset_label = request.POST.get('non_asset', False)
            csv = TEXT2CSV(asset_label)
            print_cmd(csv, NON_ASSET_BTW_FILE)
            delete_csv(csv)
        elif label_type == 'multi_asset_label':
            excel_file = request.FILES.get('files1')
            if excel_file:
                wb = openpyxl.load_workbook(excel_file)
                sheet = wb.worksheets[0]
                csv = Excel2CSV(sheet)
                print_cmd(csv)
                delete_csv(csv)

    return render(request, 'assets/label.html', locals())


#匯入Excel
def import_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('files1')
        if excel_file:
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.worksheets[0]
            for iRow in range(2, sheet.max_row+1):
                asset = Asset()
                asset.asset_no = sheet.cell(row = iRow, column = 1).value or ''
                if sheet.cell(row = iRow, column = 2).value:
                    asset.status = AssetStatus.objects.get(status_name=sheet.cell(row = iRow, column = 2).value)
                if sheet.cell(row = iRow, column = 3).value:
                    asset.category = AssetCategory.objects.get(category_name=sheet.cell(row = iRow, column = 3).value)
                if sheet.cell(row = iRow, column = 4).value:
                    asset.type = AssetType.objects.get(type_name=sheet.cell(row = iRow, column = 4).value)
                if sheet.cell(row = iRow, column = 5).value:
                    asset.brand = Brand.objects.get(brand_name=sheet.cell(row = iRow, column = 5).value)
                asset.model = sheet.cell(row = iRow, column = 6).value or ''
                asset.desc = sheet.cell(row = iRow, column = 7).value or ''
                if sheet.cell(row = iRow, column = 8).value:
                    asset.area = AssetArea.objects.get(area_name=sheet.cell(row = iRow, column = 8).value)
                asset.location = Location.objects.get(location_name=sheet.cell(row = iRow, column = 9).value)
                asset.location_desc = sheet.cell(row = iRow, column = 10).value or ''
                if sheet.cell(row = iRow, column = 11).value:
                    asset.owner_unit = Unit.objects.get(unit_name=sheet.cell(row = iRow, column = 11).value)
                if sheet.cell(row = iRow, column = 12).value:
                    asset.keeper_unit = Unit.objects.get(unit_name=sheet.cell(row = iRow, column = 12).value)
                asset.keeper_name = sheet.cell(row = iRow, column = 13).value or ''
                asset.pur_date = sheet.cell(row = iRow, column = 14).value or ''
                asset.pur_price = sheet.cell(row = iRow, column = 15).value
                asset.create_by = request.user
                asset.update_by = request.user
                asset.save()
            return redirect(get_main_url(request))

    return render(request, 'assets/import.html', locals())

#Sheet轉Table
def Sheet2Table(sheet):
    html = """<table border='1'>
                {Rows}
            </table>"""
    sRow = ""
    for iRow in range(1, sheet.max_row+1):
        sCol = ""
        for iCol in range(1, sheet.max_column+1):
            value = sheet.cell(row = iRow, column = iCol).value
            if iRow == 1:
                value = "<th>{value}</th>".format(value=value)
                sCol += value
            else:
                value = "<td>{value}</td>".format(value=value)
                sCol += value
        sCol = "<tr>" + sCol + "</tr>"
        sRow += sCol

    html = html.format(Rows=sRow)
    return html

#Sheet轉Object
def Sheet2Object(sheet):
    assets = []
    for iRow in range(2, sheet.max_row+1):
        asset = Asset()
        asset.asset_no = sheet.cell(row = iRow, column = 1).value or ''
        if sheet.cell(row = iRow, column = 2).value:
            asset.status = AssetStatus.objects.get(status_name=sheet.cell(row = iRow, column = 2).value)
        if sheet.cell(row = iRow, column = 3).value:
            asset.category = AssetCategory.objects.get(category_name=sheet.cell(row = iRow, column = 3).value)
        if sheet.cell(row = iRow, column = 4).value:
            asset.type = AssetType.objects.get(type_name=sheet.cell(row = iRow, column = 4).value)
        if sheet.cell(row = iRow, column = 5).value:
            asset.brand = Brand.objects.get(brand_name=sheet.cell(row = iRow, column = 5).value)
        asset.model = sheet.cell(row = iRow, column = 6).value or ''
        asset.desc = sheet.cell(row = iRow, column = 7).value or ''
        if sheet.cell(row = iRow, column = 8).value:
            asset.area = AssetArea.objects.get(area_name=sheet.cell(row = iRow, column = 8).value)
        asset.location = Location.objects.get(location_name=sheet.cell(row = iRow, column = 9).value)
        asset.location_desc = sheet.cell(row = iRow, column = 10).value or ''
        if sheet.cell(row = iRow, column = 11).value:
            asset.owner_unit = Unit.objects.get(unit_name=sheet.cell(row = iRow, column = 11).value)
        if sheet.cell(row = iRow, column = 12).value:
            asset.keeper_unit = Unit.objects.get(unit_name=sheet.cell(row = iRow, column = 12).value)
        asset.keeper_name = sheet.cell(row = iRow, column = 13).value or ''
        asset.pur_date = sheet.cell(row = iRow, column = 14).value or ''
        asset.pur_price = sheet.cell(row = iRow, column = 15).value
        assets.append(asset)
    return assets

#Object轉Table
def Object2Table(assets, sheet):
    html = """<table border='1'>
                {Rows}
            </table>"""
    sRow = ""
    sCol = ""
    for iCol in range(1, sheet.max_column+1):
        value = sheet.cell(row = 1, column = iCol).value or '' #若為None就回傳空字串
        value = "<th>{value}</th>".format(value=value)
        sCol += value
    sCol = "<tr>" + sCol + "</tr>"
    sRow += sCol

    for asset in assets:
        sCol = ""
        sCol += "<td>{value}</td>".format(value=asset.asset_no)
        sCol += "<td>{value}</td>".format(value=asset.status)
        sCol += "<td>{value}</td>".format(value=asset.category)
        sCol += "<td>{value}</td>".format(value=asset.type)
        sCol += "<td>{value}</td>".format(value=asset.brand)
        sCol += "<td>{value}</td>".format(value=asset.model)
        sCol += "<td>{value}</td>".format(value=asset.desc)
        sCol += "<td>{value}</td>".format(value=asset.area)
        sCol += "<td>{value}</td>".format(value=asset.location)
        sCol += "<td>{value}</td>".format(value=asset.location_desc)
        sCol += "<td>{value}</td>".format(value=asset.owner_unit)
        sCol += "<td>{value}</td>".format(value=asset.keeper_unit)
        sCol += "<td>{value}</td>".format(value=asset.keeper_name)
        sCol += "<td>{value}</td>".format(value=asset.pur_date)
        sCol += "<td>{value}</td>".format(value=asset.pur_price)

        sCol = "<tr>" + sCol + "</tr>"
        sRow += sCol

    html = html.format(Rows=sRow)
    return html

#Excel轉CSV
def Excel2CSV(sheet):
    now = datetime.now()
    file_name = datetime.strftime(now, '%Y%m%d %H%M%S') + ".csv"
    file_name = os.path.join(BASE_DIR, 'media', 'uploads', 'label', file_name)

    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = ['NUMBER']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(2, sheet.max_row+1):
            value = sheet.cell(row = i, column = 1).value
            if value:
                writer.writerow({'NUMBER': value})
    return file_name

#API預覽
def preview(request):
    result = ""
    if request.method == 'POST':
        excel_file = request.FILES.get('files1')
        if excel_file:
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.worksheets[0]
            obj = Sheet2Object(sheet)
            result = Object2Table(obj, sheet)
    return JsonResponse(result, safe=False)

#API類別
def TypeAPI(request, category_id):
    type_data = AssetType.objects.filter(category_id = int(category_id)).values('id','type_name')
    type_list = []
    for data in type_data:
        type_list.append({'id':data['id'], 'type_name':data['type_name']})

    return JsonResponse(type_list, safe = False)

#API品牌
def BrandAPI(request, category_id):
    brand_data = Brand.objects.filter(category_id = int(category_id)).values('id','brand_name')
    brand_list = []
    for data in brand_data:
        brand_list.append({'id':data['id'], 'brand_name':data['brand_name']})

    return JsonResponse(brand_list, safe = False)

#API印標籤
def print_label(request, pk):
    asset = Asset.objects.get(pk=pk)
    now = datetime.now()
    file_name = datetime.strftime(now, '%Y%m%d %H%M%S') + ".csv"
    file_name = os.path.join(BASE_DIR, 'media', 'uploads', 'label', file_name)

    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = ['NUMBER']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'NUMBER': asset.asset_no})
    print_cmd(file_name)
    delete_csv(file_name)

    return JsonResponse("success", safe = False)

