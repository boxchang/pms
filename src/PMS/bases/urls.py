from django.urls import re_path as url
from bases.views import change_status, home, index

urlpatterns = [
    url(r'^change_status$', change_status, name='change_status'),
    url(r'^', home, name='pms_home'),
    url(r'^', index, name='index'),
]
