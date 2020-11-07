from .common import *

STATIC_ROOT = '/appdata/static/'

DEBUG = False
SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = [os.environ['ALLOWED_HOST'], ]
