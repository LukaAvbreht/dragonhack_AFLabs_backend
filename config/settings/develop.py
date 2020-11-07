from .common import *

STATIC_ROOT = '/appdata/static/'

DEBUG = True
SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = [os.environ['ALLOWED_HOST'], ]
