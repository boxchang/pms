from django.conf.urls import url
from bases.views import change_status, home

urlpatterns = [
    url(r'^change_status$', change_status, name='change_status'),
    url(r'^', home, name='home'),
]