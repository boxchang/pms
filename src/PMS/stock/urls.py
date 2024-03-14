from django.urls import re_path as url
from stock.views import search

urlpatterns = [
    url(r'^search/', search, name='stock_search'),
]