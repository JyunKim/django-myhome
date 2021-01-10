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
