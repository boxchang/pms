from django.urls import re_path as url
from inventory.views import main, apply, TypeAPI, ItemAPI, detail, agree, apply_list, approve, reject, import_excel, \
    statistic, change_status, delete

urlpatterns = [
    url(r'^main/', main, name='inv_main'),
    url(r'^apply/', apply, name='inv_apply'),
    url(r'^typeapi/(?P<category_id>\d+)', TypeAPI, name='catogory_typeapi'),
    url(r'^itemapi/', ItemAPI, name='catogory_itemapi'),
    url(r'^detail/(?P<pk>\d+)/$', detail, name='inv_detail'),
    url(r'^delete/(?P<pk>\d+)/$', delete, name='inv_delete'),
    url(r'^agree/(?P<pk>\d+)/$', agree, name='inv_agree'),
    url(r'^reject/(?P<pk>\d+)/$', reject, name='inv_reject'),
    url(r'^list/', apply_list, name='inv_list'),
    url(r'^approve/', approve, name='inv_approve'),
    url(r'^import/', import_excel, name='inv_import'),
    url(r'^statistic/', statistic, name='inv_statistic'),
    url(r'^change_status/', change_status, name='inv_change_status'),

]
