from django.shortcuts import render
from django.urls import reverse
import json
from PMS.database import database
from assets.models import AssetType, AssetCategory, Asset
from borrow.forms import BorrowForm, BorrowAdminForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from borrow.models import Borrow, BorrowItem


# bootstrap sub table
def get_borrow_item_api(request, pk):
    _json = []
    items = BorrowItem.objects.filter(borrow=pk)
    for item in items:
        _json.append({"type_name": item.asset.type.type_name, "asset_no": item.asset.asset_no, "model": item.asset.model, "desc": item.asset.desc})
    return JsonResponse(_json, safe=False)


def find_asset_api(request):
    if request.method == 'POST':
        asset_no = request.POST.get('asset_no')
        asset = Asset.objects.get(asset_no=asset_no)
        name = "({status}){asset_no}　{model}　{desc}".format(status=asset.status, asset_no=asset.asset_no,
                                                            model=asset.model, desc=asset.desc)
        html = """[{{\"value\":\"{value}\", \"name\":\"{name}\"}}]""".format(value=asset_no, name=name)
    return JsonResponse(html, safe=False)


def get_asset_api(request):
    if request.method == 'POST':
        typeId = request.POST.get('typeId')
        assets = Asset.objects.filter(type=typeId, status__in=(2, 4))  # 狀態2閒置中, 狀態4出借中
        html = ""

        for asset in assets:
            name = "({status}){asset_no}　{model}　{desc}".format(status=asset.status, asset_no=asset.asset_no, model=asset.model, desc=asset.desc)
            html += """<option value="{value}">{name}</option>""".format(value=asset.asset_no, name=name)
    return JsonResponse(html, safe=False)


def get_deptuser_api(request):
    if request.method == 'POST':
        unitName = request.POST.get('unitName')
        sql = """SELECT u.id, u.userName
                  FROM Users u, Functions f, OrganizationUnit ou 
                  where leaveDate is null and f.occupantOID = u.OID and f.isMain = 1
                  and f.organizationUnitOID = ou.OID and ou.organizationUnitName = '{unitName}' and ou.validType=1""".format(unitName=unitName)
        db = database()
        rows = db.select_sql(sql)
        html = "<option value="" selected>---------</option>"

        for row in rows:
            html += """<option value="{value}">{name}</option>""".format(value=row[1], name=row[1])
    return JsonResponse(html, safe=False)


def createDeptOption():
    sql = """select id,organizationUnitName 
             from OrganizationUnit where validType = 1 and managerOID is not null order by id"""
    db = database()
    rows = db.select_sql(sql)
    html = "<option value="" selected>---------</option>"

    for row in rows:
        html += """<option value="{value}">{name}</option>""".format(value=row[1], name=row[1])
    return html


def createAssetTypeOption():
    it = AssetCategory.objects.get(category_name="資訊設備")
    types = AssetType.objects.filter(category=it)
    html = "<option value="" selected>---------</option>"

    for type in types:
        html += """<option value="{value}">{name}</option>""".format(value=type.id, name=type.type_name)
    return html


def record(request):
    return render(request, 'borrow/record.html', locals())


def apply(request):
    if request.method == 'POST':
        apply_dept = request.POST.get('apply_dept')
        apply_user = request.POST.get('apply_user')
        apply_date = request.POST.get('apply_date')
        expect_date = request.POST.get('expect_date')
        comment = request.POST.get('comment')
        borrow_list = request.POST.get('hidBorrowList')

        try:
            borrow = Borrow()
            borrow.app_dept = apply_dept
            borrow.app_user = apply_user
            borrow.comment = comment
            borrow.apply_date = apply_date
            borrow.expect_date = expect_date
            borrow.save()

            assets = borrow_list.split(",")
            for asset in assets:
                if asset:
                    item = BorrowItem()
                    item.borrow = borrow
                    item.asset = Asset.objects.get(asset_no=asset)
                    item.save()
        except Exception as e:
            print(e)

        return redirect(reverse('record'))

    form = BorrowForm()
    dept_options = createDeptOption()
    asset_type_options = createAssetTypeOption()
    return render(request, 'borrow/application.html', locals())


def update(request, pk):
    if request.method == 'POST':
        borrow = Borrow.objects.get(form_no=pk)
        if request.POST.get('lend_date'):
            borrow.lend_owner = request.user
        if request.POST.get('return_date'):
            borrow.return_owner = request.user
        form = BorrowAdminForm(request.POST, instance=borrow)
        if form.is_valid():
            tmp_form = form.save(commit=False)
            tmp_form.save()
    return render(request, 'borrow/record.html', locals())

def detail(request, form_no):
    borrow = Borrow.objects.get(form_no=form_no)
    items = borrow.borrow_item.all()
    admin_form = BorrowAdminForm()
    return render(request, 'borrow/detail.html', locals())


def form_delete(request, form_no):
    borrow = Borrow.objects.get(form_no=form_no)
    items = borrow.borrow_item.all()
    return render(request, 'borrow/detail.html', locals())


def item_delete(request, form_no):
    borrow = Borrow.objects.get(form_no=form_no)
    items = borrow.borrow_item.all()
    return render(request, 'borrow/detail.html', locals())
