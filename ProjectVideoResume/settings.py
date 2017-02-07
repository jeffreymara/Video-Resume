"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm%wptu-c93ffj3en1h&)cg7a6=4n6*k0_+1a=gf-sr_t$=_v!3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'videoresume',
    'storages',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ProjectVideoResume.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")],
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

WSGI_APPLICATION = 'ProjectVideoResume.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

DEFAULT_FILE_STORAGE = 'videoresume.aws_storage_classes.MediaStorage'
AWS_ACCESS_KEY_ID = 'AKIAIC2JUPOFASWQXOHQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'resumehost'
STATICFILES_STORAGE = 'videoresume.aws_storage_classes.StaticStorage'

AWS_S3_CUSTOM_DOMAIN = "d3o3q5kp37ae20.cloudfront.net"
#STATIC_URL = "https://%s/static/" % AWS_S3_CUSTOM_DOMAIN
STATIC_URL = "/static/"
STATICFILES_DIRS = ( os.path.join(BASE_DIR, "static"), )
MEDIA_URL = "https://%s/media/" % AWS_S3_CUSTOM_DOMAIN

#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#STATICFILES_FINDER = (
 #   "django.contrib.staticfiles.finders.FileSystemFinder",
 #   "django.contrib.staticfiles.finders.AppDirectoriesFinder"
 #)

#STATICFILES_DIRS = (
#    u'/home/videoresume/ProjectVideoResume/static',
#)

#AWS FILENAME ROOT
AWS_FILENAME_ROOT = "dev-"
