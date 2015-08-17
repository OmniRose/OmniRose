"""
Django settings for omnirose project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import local_settings

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sytf576bw)&f45=u*z8%in71o(lsywtuvg@x4g@2v0l$qxtj0a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = local_settings.DEBUG
TEMPLATE_DEBUG = local_settings.DEBUG

ALLOWED_HOSTS = []

AUTH_USER_MODEL = "accounts.User"
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/enter/'

# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'template_email',
    'bootstrapform',

    'omnirose',
    'accounts',
    'curve',
    'outputs',

    # Last so that the registration templates don't override those in accounts
    'django.contrib.admin',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'omnirose.urls'

WSGI_APPLICATION = 'omnirose.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'omnirose',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Stripe related
STRIPE_SECRET_KEY=local_settings.STRIPE_SECRET_KEY
STRIPE_PUBLIC_KEY=local_settings.STRIPE_PUBLIC_KEY

# Rose purchasing
ROSE_CURRENCY = "USD"
ROSE_PRICE    = 800 # $8

