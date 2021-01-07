import os
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = secrets["DEV_DB_SETTINGS"]
