import os
from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

DEBUG = False

ALLOWED_HOSTS = [
    'ec2-13-209-153-100.ap-northeast-2.compute.amazonaws.com',
    'www.myhome-go.com',
]

DATABASES = secrets["PROD_DB_SETTINGS"]
