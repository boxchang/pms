from django.urls import re_path as url

from users.views import *

urlpatterns = [
    url(r'^register/$', register, name='register'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^create/$', create, name='user_create'),
    url(r'^list/$', user_list, name='user_list'),
    url(r'^detail/$', detail, name='user_detail'),
    url(r'^user_edit/$', user_edit, name='user_edit'),
    url(r'^user_info/$', user_info, name='user_info'),
    url(r'^user_auth_api/$', user_auth_api, name='user_auth_api'),
]
