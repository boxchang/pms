from django.urls import re_path as url
from stock.views import search, location_setting, storage_edit

urlpatterns = [
    url(r'^search/', search, name='stock_search'),
    url(r'^location_setting/', location_setting, name='location_setting'),
    url(r'^storage_edit/', storage_edit, name='storage_edit'),
]