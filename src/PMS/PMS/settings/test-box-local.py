from .base import *

SECRET_KEY = '8i7h&)&2z!$!e710^%m)i4f(7_lpn)8ofu8&)djhix$q^66k0s'

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
