from backend.settings.base import *

DEBUG = True

ALLOWED_HOSTS = config('ALLOWED_HOSTS_ARRAY', default='', cast=lambda v: [
    s.strip() for s in v.split(',')])

CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS_ARRAY', default='', cast=lambda v: [
    s.strip() for s in v.split(',')])
