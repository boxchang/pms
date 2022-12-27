from django.urls import re_path as url
from assets.views import TypeAPI, BrandAPI, index, label, preview, main, delete, print_label, update, create, search, import_excel, detail

urlpatterns = [
    url(r'^print_label/(?P<pk>\d+)/$', print_label, name='print_label'),
    url(r'^brandapi/(?P<category_id>\d+)', BrandAPI, name='assets_brandapi'),
    url(r'^typeapi/(?P<category_id>\d+)', TypeAPI, name='assets_typeapi'),
    url(r'^import/', import_excel, name='assets_import'),
    url(r'^main/', main, name='assets_main'),
    url(r'^search/', search, name='assets_search'),
    url(r'^create/', create, name='assets_create'),
    url(r'^delete/(?P<pk>\d+)/$', delete, name='assets_delete'),
    url(r'^update/(?P<pk>\d+)/$', update, name='assets_update'),
    url(r'^detail/(?P<pk>\d+)/$', detail, name='assets_detail'),
    url(r'^preview/', preview, name='label_preview'),
    url(r'^label/', label, name='assets_label'),
    url(r'^', index, name='assets_index'),
]
