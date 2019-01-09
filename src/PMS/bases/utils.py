from enum import Enum
import datetime

from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse

from bases.models import DataIndex, FormType


# class FORM_TYPE(Enum):
#     PROJECT = 1
#     REQUEST = 2
#     PROBLEM = 3
#     BUG = 4
from projects.models import Project
from requests.models import Request_attachment


def get_all_formtype():
    formtype = {}
    objs = FormType.objects.all()
    for obj in objs:
        formtype.update({obj.form_type: obj.form_id})
    return formtype


def get_form_type(form_type):
    try:
        obj = FormType.objects.filter(type=form_type).first()
    except FormType.DoesNotExist:
        raise Http404

    return obj


def get_datetime_str():
    now = datetime.datetime.now()
    return now.strftime("%Y%m%d%H%M%S")


def get_date_str():
    now = datetime.datetime.now()
    return now.strftime("%Y%m%d")


def save_data_index(project, form_type):
    project = Project.objects.get(pk=project)
    obj = DataIndex.objects.filter(project=project, data_type=form_type.tid, data_date=get_date_str()).last()
    if obj:
        obj.current += 1
        obj.save()
    else:
        DataIndex.objects.create(project=project, data_type=form_type.tid, data_date=get_date_str(), current=1)

def get_data_index(project, form_type):
    obj = DataIndex.objects.filter(project=project, data_type=form_type.tid, data_date=get_date_str()).last()
    if obj:
        index = obj.current + 1
    else:
        index = 1
    return index

def get_serial_num(pk, form_type):
    project = Project.objects.get(pk=pk)
    no_first = project.short_name
    no_middle = get_date_str()
    no_last = form_type.short_name + str(get_data_index(project, form_type)).zfill(3)
    return no_first + no_middle + no_last

def get_form_json(form):
    json = ''
    for field in form.fields:
        json += "{field:'"+ field +"', title: '"+ form[field].label +"'},"
    json += "{'field': 'pk', 'title': '鍵值', 'visible': 'false'}"
    json = "["+json+"]"
    return json


def get_home_url(request):
    if 'project_pk' in request.session:
        return reverse('project_manage', kwargs={'pk': request.session['project_pk']})
    else:
        return reverse('login')


