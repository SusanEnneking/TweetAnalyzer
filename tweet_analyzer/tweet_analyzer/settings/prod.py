import os
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tweet_analyze_dev',
        'USER': os.getenv('PG_USER'),
        'PASSWORD': os.getenv('PG_PASSWORD'),
        'HOST': os.getenv('PG_HOST'),
        'PORT': '25060',
        'OPTIONS': {
            'sslmode': 'verify-full',
            'sslrootcert': os.path.join(BASE_DIR, 'ca-certificate.crt'),
        },
    },
}

DEBUG = True
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
WSGI_APPLICATION = 'wsgi.application'
