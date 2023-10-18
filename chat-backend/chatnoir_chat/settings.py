"""
Django settings for chatnoir_chat project.
"""

from pathlib import Path
from requests import post
from json import dumps
import yaml

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

custom_settings = {}
for cfg in (BASE_DIR / "config").glob("*.yml"):
    custom_settings.update(yaml.load(open(cfg, "r").read(), Loader=yaml.FullLoader))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = custom_settings.get("django_secret", 'django-insecure-o65%*x$!6-q&+(5u+-8$l9xgm!p(m3zavkuqbtfoob&h%q9n-h')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'chatnoir_chat',
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'chatnoir_chat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'chatnoir_chat.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if 'database' in custom_settings:
    DATABASES['default'] = {
    'ENGINE': custom_settings['database']['engine'],
    'NAME': custom_settings['database']['name'],
    'USER': custom_settings['database']['user'],
    'PASSWORD': custom_settings['database']['password'],
    'HOST': custom_settings['database']['host'],
    'PORT': int(custom_settings['database']['port']),
}

def logger_config(log_dir: Path = Path('/chatnoir_chat/logs')):
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
            'default': {
                'format': '{levelname} {asctime} {module}: {message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
        },
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
                'formatter': 'default'
            },
            'ceph_django_debug': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filters': ['require_debug_true'],
                'filename': log_dir / 'django-debug.log',
                'formatter': 'default'
            },
            'ceph_django_info': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': log_dir / 'django-info.log',
                'formatter': 'default'
            },
            'ceph_django_warn': {
                'level': 'WARNING',
                'class': 'logging.FileHandler',
                'filename': log_dir / 'django-warning.log',
                'formatter': 'default'
            },
            'ceph_tira_debug': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filters': ['require_debug_true'],
                'filename': log_dir / 'tira-debug.log',
                'formatter': 'default'
            },
            'ceph_tira_info': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': log_dir / 'tira-info.log',
                'formatter': 'default'
            },
            'ceph_tira_warn': {
                'level': 'WARNING',
                'class': 'logging.FileHandler',
                'filename': log_dir / 'tira-warning.log',
                'formatter': 'default'
            },
            'ceph_tira_db': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': log_dir / 'tira-db.log',
                'formatter': 'default'
            },
            'ceph_grpc_debug': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filters': ['require_debug_true'],
                'filename': log_dir / 'grpc-debug.log',
                'formatter': 'default'
            },
            'ceph_grpc_info': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': log_dir / 'grpc-info.log',
                'formatter': 'default'
            },
            'ceph_grpc_warn': {
                'level': 'WARNING',
                'class': 'logging.FileHandler',
                'filename': log_dir / 'grpc-warning.log',
                'formatter': 'default'
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'ceph_django_debug', 'ceph_django_warn', 'ceph_django_info'],
                'propagate': True,
            },
            'django.requests': {
                'handlers': ['console', 'ceph_django_debug', 'ceph_django_warn', 'ceph_django_info'],
                'propagate': True,
            },
            'django.server': {
                'handlers': ['console', 'ceph_django_debug', 'ceph_django_warn', 'ceph_django_info'],
                'propagate': True,
            },
            'tira': {
                'handlers': ['console', 'ceph_tira_debug', 'ceph_tira_warn', 'ceph_tira_info'],
                'propagate': True,
            },
            'tira_db': {
                'handlers': ['console', 'ceph_tira_db'],
                'propagate': True,
            },
            'grpc_server': {
                'handlers': ['console', 'ceph_grpc_debug', 'ceph_grpc_warn', 'ceph_grpc_info'],
                'propagate': True,
            },
        }
    }

LOGGING = logger_config()

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Berlin'

USE_L10N = True

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'


STATICFILES_DIRS = [
    BASE_DIR / "static/",
    BASE_DIR / "static/ui",
]

STATIC_ROOT = "/var/www/static"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

def alpacca_end_point(url: str, input_sentence: str) -> str:
    data = dumps({"input_sentence": input_sentence})
    headers = {"Content-Type": "application/json", "Accept": "application/json", "X-Disraptor-Groups": ',admins,'}

    response = post(url, data=data, headers=headers)
    response.raise_for_status()
    response_json = response.json()

    if "response" not in response_json:
        raise ValueError(f"Invalid ChatNoir Chat response: {response_json}")

    return response_json["response"]

STATIC_CHAT_ENDPOINTS = {
    'alpaca-en-7b': lambda i: alpacca_end_point('http://chatnoir-chat-gpu:5000/generate', i),
    'gpt2-xl': lambda i: alpacca_end_point('http://chatnoir-chat-gpt2-xl:5000/generate', i),
    'echo': lambda r: r,
}

PUBLIC_CHAT_ENDPOINTS = set(['alpaca-en-7b', 'gpt2-xl'])

from chatnoir_chat import custom_backends
custom_backends.websocket_server_in_background()
