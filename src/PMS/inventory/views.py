import json
from datetime import datetime
import openpyxl
from django.db import connection
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from bases.utils import django_go_sql, get_invform_status_dropdown
from inventory.forms import OfficeInvForm, InvAppliedHistoryForm
from inventory.models import ItemType, Item, AppliedForm, FormStatus, AppliedItem, Series
from users.models import CustomUser, Unit
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


# 滾序號
def get_series_number(_key, _key_name):
    obj = Series.objects.filter(key=_key)
    if obj:
        _series = obj[0].series + 1
        obj.update(series=_series, desc=_key_name)
    else:
        _series = 1
        Series.objects.create(key=_key, series=1, desc=_key_name)
    return _series


def statistic(request):
    item_map = []
    with connection.cursor() as cursor:
        sql = """select item_code,spec,cost_center,unitId,unitName, sum(qty) sum_qty from inventory_appliedform a, inventory_applieditem b, users_unit c 
                 where a.form_no = b.applied_form_id and a.unit_id = c.id
                    and a.status_id=2
                    group by item_code,spec,cost_center,unitId,unitName"""
        rows = django_go_sql(sql)

        item_map = (list(set((dic["spec"] for dic in rows))))
        unit_map = (list(set((dic["unitName"] for dic in rows))))

    html_row = "<table border='1' class='table table-bordered table-striped'>"
    # 部門HEADER
    html_row += "<tr><td style='width:200px'></td>"
    for unit_data in unit_map:
        html_row += "<td style='text-align:center;width:50px;'>" + unit_data + "</td>"
    html_row += "<td style='text-align:center;width:50px'>加總</td>"
    html_row += "</tr>"

    # 統計數值
    for item_data in item_map:
        sum_qty = 0
        html_row += "<tr><td>"+item_data+"</td>"
        for unit_data in unit_map:
            value = ""
            for row in rows:
                if row["spec"]==item_data and row["unitName"]==unit_data:
                    value = row["sum_qty"]
                    sum_qty += value
            if value:
                html_row += "<td style='text-align:right;'>"+str(value)+"</td>"
            else:
                html_row += "<td style='text-align:right;'>0</td>"
        html_row += "<td style='text-align:right;color:blue;font-weight:bold;'>"+str(sum_qty)+"</td>"
        html_row += "</tr>"
    html_row += "</table>"


    return render(request, 'inventory/statistic.html', locals())


# 回主頁
def main(request):
    form = OfficeInvForm()

    return render(request, 'inventory/application.html', locals())


def import_excel(request):
    if request.method == 'POST':
        try:
            excel_file = request.FILES.get('files1')
            if excel_file:
                wb = openpyxl.load_workbook(excel_file)
                sheet = wb.worksheets[0]
                for iRow in range(2, sheet.max_row+1):
                    if not sheet.cell(row=iRow, column=1).value:
                        break
                    type = sheet.cell(row=iRow, column=2).value
                    type = ItemType.objects.get(type_name=type)
                    vendor_code = sheet.cell(row=iRow, column=3).value
                    spec = sheet.cell(row=iRow, column=4).value
                    unit = sheet.cell(row=iRow, column=5).value
                    price = sheet.cell(row=iRow, column=7).value

                    item = Item()
                    _key = type.category.catogory_code+type.type_code
                    _key_name = type.type_name
                    series = get_series_number(_key, _key_name)
                    item.item_code = item_code = type.category.catogory_code+type.type_code+str(series).zfill(5)
                    item.item_type = type
                    item.vendor_code = vendor_code
                    item.spec = spec
                    item.unit = unit
                    item.price = price
                    item.create_by = request.user
                    item.update_by = request.user
                    item.save()
        except Exception as e:
            print(e)

    return render(request, 'inventory/import.html', locals())


def apply_list(request):
    exclude_list = [4, 5, 6]
    if request.user:
        list = AppliedForm.objects.filter(Q(requester=request.user)|Q(approver=request.user))
    if request.user.has_perm("perm_misc_apply"):
        list = AppliedForm.objects.all()

    if request.method == 'POST':
        _status = request.POST['status']
        _start_date = str(request.POST['start_date']).replace('/', '-')
        _due_date = str(request.POST['due_date']).replace('/', '-')

        if _status:
            list = list.filter(status=_status)

        if _start_date and _due_date:
            list = list.filter(apply_date__gte=_start_date, apply_date__lte=_due_date)
        form = InvAppliedHistoryForm(request.POST)
    else:
        list = list.exclude(status__in=exclude_list)
        form = InvAppliedHistoryForm()


    return render(request, 'inventory/list.html', locals())


def approve(request):
    tmp_list = AppliedForm.objects.filter(status_id=1)
    list = []
    for data in tmp_list:
        if data.requester.manager == request.user:
            list.append(data)

    return render(request, 'inventory/approve.html', locals())


def agree(request, pk):
    if request.method == 'GET':
        apply = AppliedForm.objects.get(pk=pk)
        apply.status = FormStatus.objects.get(pk=2)
        apply.approver = request.user
        apply.save()
    return redirect(reverse('inv_approve'))


def reject(request, pk):
    if request.method == 'GET':
        apply = AppliedForm.objects.get(pk=pk)
        apply.status = FormStatus.objects.get(pk=6)
        apply.save()

    return redirect(reverse('inv_approve'))


def delete(request, pk):
    if request.method == 'GET':
        apply = AppliedForm.objects.get(pk=pk)
        apply.delete()

    return redirect(reverse('inv_list'))


def apply(request):
    if request.method == 'POST':
        hidCart_list = request.POST.get('hidCart_list')
        if hidCart_list:
            items = json.loads(hidCart_list)

        unit = request.POST.get('unit')
        requester = request.POST.get('requester')
        apply_date = request.POST.get('apply_date')
        ext_number = request.POST.get('ext_number')
        reason = request.POST.get('reason')

        try:
            apply = AppliedForm()
            apply.unit = Unit.objects.get(pk=unit)
            apply.requester = CustomUser.objects.get(emp_no=requester)
            apply.apply_date = apply_date
            apply.ext_number = ext_number
            apply.reason = reason
            apply.status = FormStatus.objects.get(pk=1)
            apply.create_by = request.user
            apply.save()

            for item in items:
                obj = AppliedItem()
                obj.item_code = item['item_code']
                obj.spec = item['spec']
                obj.price = item['price']
                obj.qty = item['qty']
                obj.unit = item['unit']
                obj.amount = item['total']
                obj.applied_form = apply
                obj.save()

        except Exception as e:
            print(e)

        return redirect(apply.get_absolute_url())

    form = OfficeInvForm()
    return render(request, 'inventory/application.html', locals())


def detail(request, pk):
    try:
        total_price = 0
        form = AppliedForm.objects.get(pk=pk)
        for item in form.applied_form_item.all():
            total_price += item.amount
        status_html = get_invform_status_dropdown(form)

        if form.status.id == 1 and form.requester.manager == request.user:
            isApprover = True

        if form.requester == request.user:
            isCreater = True

    except AppliedForm.DoesNotExist:
        raise Http404('Form does not exist')


    return render(request, 'inventory/detail.html', locals())


#API類別
def TypeAPI(request, category_id):
    type_data = ItemType.objects.filter(category_id = int(category_id)).values('id','type_name')
    type_list = []
    for data in type_data:
        type_list.append({'id':data['id'], 'type_name':data['type_name']})

    return JsonResponse(type_list, safe = False)


#API類別
def ItemAPI(request):
    item_list = []
    if request.method == 'POST':
        type_id = request.POST.get('type_id')
        keyword = request.POST.get('keyword')
        item_data = Item.objects.all()
        if type_id:
            item_data = item_data.filter(item_type_id=int(type_id)).values('item_code', 'spec', 'price', 'unit')
        if keyword:
            query = Q(spec__icontains=keyword)
            item_data = item_data.filter(query).values('item_code', 'spec', 'price', 'unit')

        for data in item_data:
            item_list.append({'item_code':data['item_code'], 'spec':data['spec'], 'price':data['price'], 'unit':data['unit']})

    return JsonResponse(item_list, safe = False)


def change_status(request):
    if request.POST:
        form_id = request.POST.get('form_id')
        status_id = request.POST.get('status_id')

        status = FormStatus.objects.get(pk=status_id)
        obj = AppliedForm.objects.get(pk=form_id)
        obj.status = status
        obj.save()

        return redirect(obj.get_absolute_url())


def mail_test(request):
    # 電子郵件內容樣板
    email_template = render_to_string(
        'inventory/email_template.html',
        {'username': request.user.username}
    )
    email = EmailMessage(
        '註冊成功通知信',  # 電子郵件標題
        email_template,  # 電子郵件內容
        settings.EMAIL_HOST_USER,  # 寄件者
        ['hsiangchih.chang@tw.eagleburgmann.com']  # 收件者
    )
    email.fail_silently = False
    email.send()