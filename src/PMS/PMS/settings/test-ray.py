# PMS/settings/test-nico.py

from .test import *

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.mysql',
        # Or path to database file if using sqlite3.
        'NAME': 'prog_pms',                      # DB name
        'USER': 'ray',                       # Not used with sqlite3.
        'PASSWORD': 'Ss770609',               # Not used with sqlite3.
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '10.231.0.28',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '3306',
    },
}