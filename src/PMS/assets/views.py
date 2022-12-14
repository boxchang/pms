#!/usr/bin/python
# coding=utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from assets.models import Label_attachment
import openpyxl
from django.http import JsonResponse
import os
from PMS.settings.base import BTW_FILE, EXE_FILE, PRINTER, BASE_DIR
import csv


def print_cmd(EXCEL_FILE):
    CMD = """{EXE_FILE} /AF=\"{BTW_FILE}\" /D=\"{EXCEL_FILE}\" /PRN=\"{PRINTER}\" /P/X""".format(EXE_FILE=EXE_FILE, BTW_FILE=BTW_FILE, EXCEL_FILE=EXCEL_FILE, PRINTER=PRINTER)
    print(CMD)
    os.system(CMD)

@login_required
def index(request):
    return render(request, 'assets/index.html', locals())

def Sheet2Table(sheet):
    html = """<table>
                <tr>
                    <th>NUMBER</th>
                </tr>
                {label}
            </table>"""
    label = ""
    for i in range(2, sheet.max_row+1):
        value = sheet.cell(row = i, column = 1).value
        print(sheet.cell(row = i, column = 1).value)
        if value:
            value = "<tr><td>{value}</td></tr>".format(value=value)
            label += value
        else:
            break

    html = html.format(label=label)
    return html

def Excel2CSV(sheet):
    from datetime import datetime

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

def delete_csv(file_name):
    try:
        os.remove(file_name)
    except OSError as e:
        print(e)
    else:
        print("File is deleted successfully")

@login_required
def label(request):
    if request.method == 'POST':
        # if request.FILES.get('files1'):
        #     request_file = Label_attachment(files=request.FILES['files1'])
        #     request_file.description = request.POST['description1']
        #     request_file.create_by = request.user
        #     request_file.save()
        #     print_cmd(request_file.files.path)

        excel_file = request.FILES.get('files1')
        if excel_file:
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.worksheets[0]
            csv = Excel2CSV(sheet)
            print_cmd(csv)
            delete_csv(csv)

    return render(request, 'assets/label.html', locals())

def preview(request):
    result = ""
    if request.method == 'POST':
        excel_file = request.FILES.get('files1')
        if excel_file:
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.worksheets[0]
            result = Sheet2Table(sheet)
    return JsonResponse(result, safe=False)


