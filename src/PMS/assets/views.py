#!/usr/bin/python
# coding=utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from assets.models import Label_attachment
import openpyxl
from django.http import JsonResponse
import os

def print_cmd(cmd):
    EXE_FILE = "C:\\\"Program Files (x86)\"\\Seagull\\\"BarTender Suite\"\\bartend.exe"
    BTW_FILE = "C:\\Users\\hsiangchih.chang\\Desktop\\Temp\\template.btw"
    EXCEL_FILE = "C:\\Users\\hsiangchih.chang\\Desktop\\Temp\\Bartender_List.xlsx"
    PRINTER = "Microsoft Print to PDF"
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

@login_required
def label(request):
    if request.method == 'POST':
        if request.FILES.get('files1'):
            request_file = Label_attachment(files=request.FILES['files1'])
            request_file.description = request.POST['description1']
            request_file.create_by = request.user
            #request_file.save()
            print_cmd("")

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


