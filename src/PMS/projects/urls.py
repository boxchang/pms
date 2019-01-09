from django.conf.urls import url

from projects.ajax_views import getChild, getChildByProj, getAllProblem, getBug
from projects.views import *

urlpatterns = [
    url(r'^$', index),
    url(r'^edit/(?P<pk>\d+)/$', project_edit, name="project_edit"),
    url(r'^delete/(?P<pk>\d+)/$', project_delete, name="project_delete"),
    url(r'^add/$', project_create, name="project_create"),
    url(r'^list/$', project_list, name="project_list"),
    url(r'^manage/(?P<pk>\d+)/$', project_manage, name="project_manage"),
    url(r'^manage/\d+/getChild/(?P<pk>\d+)/$', getChild, name="getChild"),
    url(r'^manage/\d+/getChildByProj/(?P<pk>\d+)/$', getChildByProj, name="getChildByProj"),
    url(r'^manage/\d+/getProblem/(?P<pk>\d+)/$', getAllProblem, name="getProblem"),
    url(r'^manage/\d+/getBug/(?P<pk>\d+)/$', getBug, name="getBug"),
    url(r'^setting/$', project_setting, name="project_setting"),
    url(r'^search/$', search, name="search"),
]
