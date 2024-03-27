# PMS/settings/production.py

from .base import *

PROD = True

SECRET_KEY = '8i7h&)&2z!$!e710^%m)i4f(7_lpn)8ofu8&)djhix$q^66k0s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.mysql',
        # Or path to database file if using sqlite3.
        'NAME': 'nico',
        'USER': 'nico',                       # Not used with sqlite3.
        'PASSWORD': 'nicodb#123',               # Not used with sqlite3.
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': 'git-runner.it.srv.dc',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '3306',
    },
}