from django.urls import re_path as url
from assets.views import index, label, preview

urlpatterns = [
    url(r'^preview/', preview, name='label_preview'),
    url(r'^label/', label, name='assets_label'),
    url(r'^', index, name='assets_index'),
]
