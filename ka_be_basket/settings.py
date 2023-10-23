"""
Django settings for ka_be_basket project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
# import logging
import os
import sys
from collections import OrderedDict
from decimal import Decimal
from decimal import ROUND_DOWN
from pathlib import Path

import dj_database_url
from corsheaders.defaults import default_headers
from oscar.defaults import *  # noqa
# from oscar import get_core_apps
# from oscar import OSCAR_MAIN_TEMPLATE_DIR

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'KAStarter')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.getenv('DEBUG') == 'True' else False

ALLOWED_HOSTS = ['*']
if os.getenv('REMOTE_HOST_URL'):
    ALLOWED_HOSTS += [
        os.getenv('REMOTE_HOST_URL')
    ]


def location(x):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), x)


def is_run_in_test_env():
    return len(sys.argv) > 1 and sys.argv[1] == 'test'


def is_run_in_prod_env():
    return os.getenv('DJANGO_ENV') == 'production'


def is_run_in_docker_env():
    return os.getenv('DOCKER_ENV') == 'True'


IS_RUN_IN_DOCKER_ENV = is_run_in_docker_env()
IS_RUN_IN_TEST_ENV = is_run_in_test_env()
IS_RUN_IN_PROD_ENV = is_run_in_prod_env()


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_su',  # for admin to login as other user, put before django.contrib.admin
    'django.contrib.admin',
    'rest_framework',
    'corsheaders',
    'django_rq',

    'django.contrib.sites',
    'django.contrib.flatpages',

    'oscar.config.Shop',
    'oscar.apps.analytics.apps.AnalyticsConfig',
    'oscar.apps.checkout.apps.CheckoutConfig',
    'oscar.apps.address.apps.AddressConfig',
    'oscar.apps.shipping.apps.ShippingConfig',
    'oscar.apps.catalogue.apps.CatalogueConfig',
    'oscar.apps.catalogue.reviews.apps.CatalogueReviewsConfig',
    'oscar.apps.communication.apps.CommunicationConfig',
    'oscar.apps.partner.apps.PartnerConfig',
    'oscar.apps.basket.apps.BasketConfig',
    'oscar.apps.payment.apps.PaymentConfig',
    'oscar.apps.offer.apps.OfferConfig',
    'oscar.apps.order.apps.OrderConfig',
    'oscar.apps.customer.apps.CustomerConfig',
    'oscar.apps.search.apps.SearchConfig',
    'oscar.apps.voucher.apps.VoucherConfig',
    'oscar.apps.wishlists.apps.WishlistsConfig',
    'oscar.apps.dashboard.apps.DashboardConfig',
    'oscar.apps.dashboard.reports.apps.ReportsDashboardConfig',
    'oscar.apps.dashboard.users.apps.UsersDashboardConfig',
    'oscar.apps.dashboard.orders.apps.OrdersDashboardConfig',
    'oscar.apps.dashboard.catalogue.apps.CatalogueDashboardConfig',
    'oscar.apps.dashboard.offers.apps.OffersDashboardConfig',
    'oscar.apps.dashboard.partners.apps.PartnersDashboardConfig',
    'oscar.apps.dashboard.pages.apps.PagesDashboardConfig',
    'oscar.apps.dashboard.ranges.apps.RangesDashboardConfig',
    'oscar.apps.dashboard.reviews.apps.ReviewsDashboardConfig',
    'oscar.apps.dashboard.vouchers.apps.VouchersDashboardConfig',
    'oscar.apps.dashboard.communications.apps.CommunicationsDashboardConfig',
    'oscar.apps.dashboard.shipping.apps.ShippingDashboardConfig',

    # 3rd-party apps that oscar depends on
    'widget_tweaks',
    'haystack',
    'treebeard',
    # 'sorl.thumbnail',   # Default thumbnail backend, can be replaced
    'django_tables2',

    'oscarapi',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'ka_be_basket.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            location('templates'),
            # OSCAR_MAIN_TEMPLATE_DIR,
        ],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # 'oscar.apps.promotions.context_processors.promotions',

                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.communication.notifications.context_processors.notifications',
                'oscar.core.context_processors.metadata',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                # 'django.template.loaders.eggs.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = 'ka_be_basket.wsgi.application'


'''
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   Caches
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
'''
CACHES = {}
rediscloud_url = os.getenv('REDISCLOUD_URL')
if rediscloud_url is not None:
    CACHES["default"] = {
        "BACKEND": "django_redis.cache.RedisCache",
        # If you're on Heroku
        "LOCATION": rediscloud_url,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "REDIS_CLIENT_KWARGS": {
                "health_check_interval": 30,
            },
        }
    }
else:
    CACHES["default"] = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }

CACHES["django-rq"] = {
    "BACKEND": "django_redis.cache.RedisCache",
    # If you're on Heroku
    "LOCATION": os.getenv('REDISCLOUD_MAUVE_URL', 'redis://localhost:6379'),
    "OPTIONS": {
        "CLIENT_CLASS": "django_redis.client.DefaultClient",
        'DB': 0,
        "REDIS_CLIENT_KWARGS": {
            "health_check_interval": 30,
        },
    }
}

# Long cache timeout for staticfiles, since this is used heavily by the optimizing storage.
CACHES['staticfiles'] = {
    "BACKEND": CACHES['default']['BACKEND'],
    "TIMEOUT": 60 * 60 * 24 * 365,
    "LOCATION": "staticfiles",
}


'''
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   RQ
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
'''
RQ_QUEUES = {
    'high': {
        'USE_REDIS_CACHE': 'django-rq',
        'DEFAULT_TIMEOUT': 300,
    },
    'default': {
        'USE_REDIS_CACHE': 'django-rq',
        'DEFAULT_TIMEOUT': 300,
    },
    'low': {
        'USE_REDIS_CACHE': 'django-rq',
        'DEFAULT_TIMEOUT': 300,
    },
    'very-low': {
        'USE_REDIS_CACHE': 'django-rq',
        'DEFAULT_TIMEOUT': 420,
    },
    'publisher': {
        'USE_REDIS_CACHE': 'django-rq',
        'DEFAULT_TIMEOUT': 300,
    },
    'stockrecord': {
        'USE_REDIS_CACHE': 'django-rq',
        'DEFAULT_TIMEOUT': 300,
    },
    'migration': {
        'USE_REDIS_CACHE': 'django-rq',
        'DEFAULT_TIMEOUT': 300,
    },
    'stocksyncreport': {
        'USE_REDIS_CACHE': 'django-rq',
        'DEFAULT_TIMEOUT': 300,
    },
}
if IS_RUN_IN_DOCKER_ENV or IS_RUN_IN_TEST_ENV:
    queue_channel_settings = {
        'URL': 'redis://172.20.0.7:6379',
        'DEFAULT_TIMEOUT': 300,
        'DB': 0,
    } if IS_RUN_IN_DOCKER_ENV else {
        'URL': 'redis://localhost:6379',
        'DEFAULT_TIMEOUT': 300,
        'DB': 0,
    }
    RQ_QUEUES = {
        'high': queue_channel_settings,
        'default': queue_channel_settings,
        'low': queue_channel_settings,
        'very-low': queue_channel_settings,
        'publisher': queue_channel_settings,
        'stockrecord': queue_channel_settings,
        'migration': queue_channel_settings,
        'stocksyncreport': queue_channel_settings,
    }

RQ_SHOW_ADMIN_LINK = True


'''
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   Django Settings (non oscar)
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
'''

# we're not using tablespaces, when it applies, migration to old files will be affected
# DEFAULT_TABLESPACE = 'ka_be_basket'

# set cookie domain to REMOTE_HOST_URL
# this include its subdomain as well
SESSION_COOKIE_DOMAIN = os.getenv('REMOTE_HOST_URL')

# disable https cookie on local dev
SESSION_COOKIE_SECURE = False
if IS_RUN_IN_PROD_ENV or os.getenv('REMOTE_HOST_URL'):
    SESSION_COOKIE_SECURE = True


SITE_ID = 1


# Authentication Backends
AUTHENTICATION_BACKENDS = [
    'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
    'django_su.backends.SuBackend'
]

REST_FRAMEWORK = {
    'CHARSET': 'utf-8',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        # 'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        # 'rest_framework_csv.renderers.CSVRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': [
        # 'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
    ],
    # 'EXCEPTION_HANDLER': 'ka_be_basket.api.utils.exceptions.custom_exception_handler',
    # 'DEFAULT_PAGINATION_CLASS': 'ka_be_basket.api.framework.pagination.CustomPagination',
    # 'PAGE_SIZE': 10,
    'MAX_PAGE_SIZE': 1500,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

# CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True  # it can't be used together with CORS_ALLOW_CRDENTIALS
CORS_ALLOW_HEADERS = (
    *default_headers,
    'api-key',
    'user-auth-token',
    'partner-api-key',
    'x-requested-with',
    'x-hub-signature',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'user-agent',
    'accept-encoding',
    'session-id',
    'cache-control',
    'zone-code',
)


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
IS_USING_ENV_CREDS = all(key in os.environ for key in [
                         'DB_CRED_USERNAME', 'DB_CRED_HOST', 'DB_CRED_NAME', 'DB_CRED_PASSWORD'])
if IS_USING_ENV_CREDS and not IS_RUN_IN_TEST_ENV:  # Use database credentials from environment variables
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'PORT': 5432,
            'USER': os.getenv('DB_CRED_USERNAME', 'postgres'),
            'HOST': os.getenv('DB_CRED_HOST', 'localhost'),
            'NAME': os.getenv('DB_CRED_NAME', 'postgres'),
            'PASSWORD': os.getenv('DB_CRED_PASSWORD', ''),
            'CONN_MAX_AGE': 100,
        }
    }
elif IS_RUN_IN_DOCKER_ENV and not IS_RUN_IN_TEST_ENV:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'password',
            'HOST': 'ka-be-basket-db',
            'PORT': 5432,
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.config(
            default='sqlite:///{0}'.format(location('db.sqlite')))
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Jakarta'  # TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = location('public/static')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = location("public/media")
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

'''
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   Email Related Settings
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
'''

EMAIL_SUBJECT_PREFIX = '[XYZ] '
OSCAR_FROM_EMAIL = 'hello@xyz.com'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

SYSTEM_FROM_EMAIL = 'system@xyz.com'


'''
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   Oscar Settings
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
'''
# ==========
# Meta
# ==========

# Display settings
OSCAR_SHOP_NAME = 'XYZ Corp.'
OSCAR_SHOP_TAGLINE = 'Bring Innovations to the World'

# Currency settings
OSCAR_DEFAULT_CURRENCY = 'IDR'

# Offer settings


def round_offer_function(amount):
    return amount.quantize(Decimal('1.'), rounding=ROUND_DOWN)


OSCAR_OFFER_ROUNDING_FUNCTION = round_offer_function

# Checkout settings
OSCAR_ALLOW_ANON_CHECKOUT = True

# This is needed for the hosted version of the sandbox
# ADMINS = (
#     ('Michael Susanto', 'michael.susanto21@ui.ac.id')
# )
# MANAGERS = ADMINS

OSCAR_INITIAL_ORDER_STATUS = 'Pending'

VOID_ORDER_STATUS = 'Void (Freezed)'
COMPLETED_ORDER_STATUS = 'Completed (Freezed)'
CANCEL_ORDER_STATUS = '-- Cancel'
ORDER_CANCEL_STATUSES = [VOID_ORDER_STATUS, CANCEL_ORDER_STATUS]


# ================
# Order Pipeline
# ================

pipeline = OrderedDict({})  # noqa

# pipeline[VOID_ORDER_STATUS] = (
#     'Pending',
#     CANCEL_ORDER_STATUS,
# )

pipeline[COMPLETED_ORDER_STATUS] = ()
pipeline[VOID_ORDER_STATUS] = ()

pipeline[CANCEL_ORDER_STATUS] = (
    VOID_ORDER_STATUS,
    'Pending',
)

pipeline['Pending'] = (
    COMPLETED_ORDER_STATUS,
    CANCEL_ORDER_STATUS,
)

# Backward compatibility to allow it to be marked as void/delivered
# Breaking order flow change on 7 Feb
pipeline['Issue to Made To Order'] = \
    pipeline['Start Manufacturing'] = \
    pipeline['Issue to Merchant'] = \
    pipeline['Ready To Deliver'] = \
    pipeline['M Ready To Deliver'] = \
    pipeline['Delivered To CUSTOMER'] = \
    pipeline['Prep Delivery To CUSTOMER'] = \
    pipeline['In Transit To CUSTOMER'] = \
    pipeline['Prep Delivery To XYZ'] = \
    pipeline['In Transit To XYZ'] = \
    pipeline['Delivered To XYZ'] = \
    (
    COMPLETED_ORDER_STATUS,
    CANCEL_ORDER_STATUS,
)
# End Backward compatibility

OSCAR_ORDER_STATUS_PIPELINE = pipeline

order_status_pipeline_final = []
for (key, value) in pipeline.items():
    if not len(value):
        order_status_pipeline_final.append(key)
OSCAR_ORDER_STATUS_PIPELINE_FINAL = order_status_pipeline_final


# =====================
# Order Line Pipeline
# =====================

PENDING_LINE_STATUS = 'Pending'
CANCELLED_LINE_STATUS = 'Cancelled'
COMPLETED_LINE_STATUS = 'Completed'

line_pipeline = OrderedDict({})  # noqa
line_pipeline[PENDING_LINE_STATUS] = (
    CANCELLED_LINE_STATUS
)

OSCAR_INITIAL_LINE_STATUS = PENDING_LINE_STATUS
OSCAR_LINE_STATUS_PIPELINE = line_pipeline

'''
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   Haystack Settings
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
'''

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

'''
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   Oscarapi Settings
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
'''


OSCARAPI_BLOCK_ADMIN_API_ACCESS = False

OSCAR_EAGER_ALERTS = False
OSCAR_BASKET_COOKIE_LIFETIME = 604800 * 4 * \
    6  # (1 week in seconds * 4 * 6 = 6 months)
