from django.conf.urls import url

from problems.views import *

urlpatterns = [
    url(r'^edit/(?P<pk>\d+)/$', problem_edit, name="problem_edit"),
    url(r'^add/$', problem_create, name="problem_create"),
    url(r'^list/$', problem_list, name="problem_list"),
    url(r'^detail/(?P<pk>\d+)/$', problem_detail, name="problem_detail"),
    url(r'^delete/(?P<pk>\d+)/$', problem_delete, name="problem_delete"),
    url(r'^reply/(?P<pk>\d+)/$', problem_reply_create, name="problem_reply_create"),
    url(r'^pfd/(?P<pk>\d+)/$', problem_file_delete, name="problem_file_delete"),
]