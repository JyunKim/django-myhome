import os
from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = False

ALLOWED_HOSTS = [
    'myhome-go.com',
    'www.myhome-go.com',
]

DATABASES = secrets["PROD_DB_SETTINGS"]

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'
STATICFILES_STORAGE = 'config.storages.StaticStorage'

AWS_ACCESS_KEY_ID = secrets["ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = secrets["SECRET_ACCESS_KEY"]
AWS_STORAGE_BUCKET_NAME = secrets["BUCKET_NAME"]
AWS_S3_REGION_NAME = secrets["REGION_NAME"]
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME)
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
