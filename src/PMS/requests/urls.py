from django.conf.urls import url

from projects.ajax_views import *
from requests.views import *

urlpatterns = [
    url(r'^edit/(?P<pk>\d+)/$', request_edit, name="request_edit"),
    url(r'^add/$', request_create, name="request_create"),
    url(r'^list/$', request_list, name="request_list"),
    url(r'^detail/(?P<pk>\d+)/$', request_detail, name="request_detail"),
    url(r'^delete/(?P<pk>\d+)/$', request_delete, name="request_delete"),
    url(r'^$', get_request, name="get_request"),
    url(r'^index/(?P<pk>\d+)/$', request_index, name="request_index"),
    url(r'^receive', request_receive, name="request_receive"),
    url(r'change_status', change_status, name="change_status"),
    url(r'^rfd/(?P<pk>\d+)', request_file_delete, name="request_file_delete"),
    url(r'^(?P<no>\w+)$', request_guest, name="request_guest"),
]