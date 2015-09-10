"""
Django settings for OTAutoSearch project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mj=m7qe+9w2n33v&)@qf3&yzhon2fja+j8slvte0j66-v3o7f!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    #'south',
    #'registration',
    #'registration_email',
    'OTobjects',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'OTAutoSearch.urls'

WSGI_APPLICATION = 'OTAutoSearch.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME':'OTdb',
        'USER':'minigwac',
        'PASSWORD':'gwac',
        'HOST':'',
        'PORT':'5439',
    }
}

# Caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'utf-8'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

#-User custom variables
HOME = os.path.expanduser('~')
base_path = os.path.join(HOME,'work/miniGWAC/test/otpredict')
static_path = os.path.join(HOME,'projects/django/OTAutoSearch/OTobjects/static')


#-User registration
#ACCOUNT_ACTIVATION_DAYS = 7
#AUTHENTICATION_BACKENDS = (
#    'registration_email.auth.EmailBackend',
#)
# NOTICE:not work `lambda request, user: '/'`
#LOGIN_REDIRECT_URL = '/ot/index/'
# NOTICE:not work only '/accounts/activate/complete/'
#REGISTRATION_EMAIL_ACTIVATE_SUCCESS_URL = lambda request, user: '/accounts/activate/complete/'
#REGISTRATION_EMAIL_REGISTER_SUCCESS_URL = lambda request, user: '/accounts/register/complete/'
