"""
Django settings for VirtualJudge project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8*5dsvla=-uj53$5hfqmm6qhg4)357l0dyk=%l$8feo#^cpbd='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 允许访问的网址

ALLOWED_HOSTS = ['', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'django.contrib.staticfiles', 引用静态文件
    'Authentication',
    'Problem',
    'mongoengine',
    'djcelery',     # django-celery必须添加
    'corsheaders',  # 跨域请求
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 跨域请求，注意顺序，在'django.middleware.common.CommonMiddleware',之前
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'CloudJudge.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'CloudJudge.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# mysql

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'virtual_schema',
        #'HOST': '',
        'HOST': '',
        'PORT': '',
        'USER': '',
        'PASSWORD': '',
        'CHARSET': 'UTF8',
    },
}

import pymysql
pymysql.install_as_MySQLdb()

# mongodb

MONGODB_DATABASES = {
    "default": {
        'NAME': '',
        # 'HOST': '127.0.0.1',
        'HOST': '',
        'PORT': '',
        'USERNAME': '',
        'PASSWORD': '',
        "tz_aware": True,  # 设置时区
    },
}
from mongoengine import connect
# connect('cloud', host='', port=, username='', password='')
connect('cloud', host='', port=, username='', password='')

# redis

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # "LOCATION": "",
        "LOCATION": "redis://",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": ""
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

# 设置时区
# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# 配置Broker
BROKER_URL = 'redis://:@'
BROKER_TRANSPORT = 'redis'

# 邮箱配置

# 与SMTP服务器通信时，是否启动TLS链接(安全链接)。默认是false
# EMAIL_USE_TLS = True
# 163 ssl协议端口号：465/994 非ssl端口号:25

EMAIL_USE_SSL = True
EMAIL_HOST = ''  # 如果是 163 改成 smtp.163.com
EMAIL_PORT = 
EMAIL_HOST_USER = '' # 帐号
EMAIL_HOST_PASSWORD = ''  # 密码
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_SUBJECT_PREFIX = '[]'  # 为邮件Subject-line前缀,默认是'[django]'
# 管理员站点
# The email address that error messages come from, such as those sent to ADMINS and MANAGERS.
SERVER_EMAIL = ''


# 跨域增加忽略

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    '*'
)

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)
