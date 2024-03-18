from django.urls import re_path as url
from stock.views import search, location_setting, storage_edit, location_list, location_add, location_edit, \
    location_save, bin_add, bin_edit, bin_save, bin_list, stock_in, stock_out

urlpatterns = [
    url(r'^search/', search, name='stock_search'),
    url(r'^location_setting/', location_setting, name='location_setting'),
    url(r'^location/', location_list, name='location_list'),
    url(r'^location_add/', location_add, name='location_add'),
    url(r'^location_edit/', location_edit, name='location_edit'),
    url(r'^location_save/', location_save, name='location_save'),
    url(r'^storage_edit/', storage_edit, name='storage_edit'),
    url(r'^bin/(?P<storage_code>\w+)/(?P<location_code>[\w-]+)', bin_list, name='bin_list'),
    url(r'^bin_add/', bin_add, name='bin_add'),
    url(r'^bin_edit/', bin_edit, name='bin_edit'),
    url(r'^bin_save/', bin_save, name='bin_save'),
    url(r'^stock_in/', stock_in, name='stock_in'),
    url(r'^stock_out/', stock_out, name='stock_out'),
]