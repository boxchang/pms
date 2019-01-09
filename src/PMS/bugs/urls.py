from django.conf.urls import url

from bugs.views import *
from projects.ajax_views import getProblem

urlpatterns = [
    url(r'^edit/(?P<pk>\d+)/$', bug_edit, name="bug_edit"),
    url(r'^add/$', bug_create, name="bug_create"),
    url(r'^list/$', bug_list, name="bug_list"),
    url(r'^detail/(?P<pk>\d+)/$', bug_detail, name="bug_detail"),
    url(r'^delete/(?P<pk>\d+)/$', bug_delete, name="bug_delete"),
    url(r'^bfd/(?P<pk>\d+)', bug_file_delete, name="bug_file_delete"),
    url(r'^detail/\d+/getProblem/(?P<tid>\d+)/(?P<pk>\d+)/$', getProblem, name="getBugProblem"),
]