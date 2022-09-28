import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'INSECURE')

DEBUG = 1

ALLOWED_HOSTS: list[str] = ['*']

CSRF_TRUSTED_ORIGINS = ['https://sneakers.andrepf.com/*']

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',  # noqa: E501
    'PAGE_SIZE': 10,
}
