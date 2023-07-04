from django.urls import re_path as url
from inventory.views import main, apply

urlpatterns = [
    url(r'^main/', main, name='inv_main'),
    url(r'^apply/', apply, name='inv_apply'),
]
