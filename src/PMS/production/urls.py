from django.urls import re_path as url

from production.views import excel_import, excel_import_preview, record, get_step_info, record_detail, record_edit, \
    record_del, wo_detail, record2, record2_del, get_user_info, record_detail_empno, record_manage

urlpatterns = [
    url(r'^import/', excel_import, name='prod_import'),
    url(r'^record/', record, name='prod_record'),
    url(r'^record2/', record2, name='prod_record2'),
    url(r'^record_edit/(?P<pk>\d+)/$', record_edit, name='prod_record_edit'),
    url(r'^record_delete/(?P<pk>\d+)/$', record_del, name='prod_record_del'),
    url(r'^record2_delete/(?P<pk>\d+)/$', record2_del, name='prod_record2_del'),
    url(r'^record_detail/$', record_detail, name='prod_record_detail'),
    url(r'^record_detail/(?P<emp_no>\w+)/$', record_detail_empno, name='prod_record_detail_empno'),
    url(r'^record_manage/', record_manage, name='prod_record_manage'),
    url(r'^wo_detail/', wo_detail, name='prod_wo_detail'),
    url(r'^import_preview/', excel_import_preview, name='prod_import_preview'),
    url(r'^get_step_info/', get_step_info, name='get_step_info_api'),
    url(r'^get_user_info/', get_user_info, name='get_user_info_api'),
]