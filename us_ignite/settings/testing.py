# Testing settings for us_ignite
from us_ignite.settings.base import *


SECRET_KEY = 'c!lizso+53#4dhm*o2qyh9t(n14p#wr5!+%1bfjtrqa#vsc$@h'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'us-ignite-test.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}


INSTALLED_APPS += (
    'django_nose',
)

EXCLUDED_APPS = (
    # 'south',
)

INSTALLED_APPS = filter(
    lambda a: a not in EXCLUDED_APPS, INSTALLED_APPS)


EXCLUDED_MIDDLEWARE = (
    'us_ignite.common.middleware.URLRedirectMiddleware',
)

MIDDLEWARE_CLASSES = filter(
    lambda m: m not in EXCLUDED_MIDDLEWARE, MIDDLEWARE_CLASSES)

NOSE_ARGS = [
    '-s',
    '--failed',
    '--stop',
    '--nocapture',
    '--failure-detail',
    '--with-progressive',
    # '--logging-filter=-south',
    '--with-blockage',
]


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# ignore South
# SOUTH_TESTS_MIGRATE = False
# SKIP_SOUTH_TESTS = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Faster tests with the MD5hasher.
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']


SITE_URL = 'http://testing-us-ignite.org'

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATIC_URL = '/static/'

TWITTER_API_KEY = 'api-key'
TWITTER_API_SECRET = 'api-secret'

# AWS dummy:
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = 'testing-us-ignite-dot-org'

# WP
WP_URL = 'http://wptest.org'

MAILCHIMP_API_KEY='0000000000-000'
MAILCHIMP_LIST='00000'
