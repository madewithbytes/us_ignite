# Django settings for us_ignite project.
import os
import dj_database_url

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Alfredo Aguirre', 'notifications@madewithbyt.es'),
)

MANAGERS = ADMINS

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
# settings is one directory up now
here = lambda *x: os.path.join(PROJECT_ROOT, '..', *x)


# Heroku DB requirements
DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}
# DATABASES['default']['ENGINE'] = 'django_postgrespool'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'US/Eastern'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True


US_TIMEZONES = (
    ('US/Alaska', 'US/Alaska'),
    ('US/Aleutian', 'US/Aleutian'),
    ('US/Arizona', 'US/Arizona'),
    ('US/Central', 'US/Central'),
    ('US/East-Indiana', 'US/East-Indiana'),
    ('US/Eastern', 'US/Eastern'),
    ('US/Hawaii', 'US/Hawaii'),
    ('US/Indiana-Starke', 'US/Indiana-Starke'),
    ('US/Michigan', 'US/Michigan'),
    ('US/Mountain', 'US/Mountain'),
    ('US/Pacific', 'US/Pacific'),
    ('US/Pacific-New', 'US/Pacific-New'),
    ('US/Samoa', 'US/Samoa'),
)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = here('..', 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = here('..', 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    here('assets'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
    'us_ignite.common.middleware.DoNotTrackMiddleware',
    'us_ignite.common.middleware.URLRedirectMiddleware',
    # 'lockdown.middleware.LockdownMiddleware',
)



TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django_browserid.context_processors.browserid',
    'us_ignite.common.context_processors.settings_available',
    'us_ignite.apps.context_processors.applications_context',
)

ROOT_URLCONF = 'us_ignite.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'us_ignite.wsgi.application'

TEMPLATE_DIRS = (
    here('templates'),
)

# Authentication:
AUTHENTICATION_BACKENDS = (
    'us_ignite.profiles.backends.authentication.EmailModelBackend',
    'django.contrib.auth.backends.ModelBackend',
    'django_browserid.auth.BrowserIDBackend',
)


PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django_browserid',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.redirects',
    'gunicorn',
    'compressor',
    'registration',
    'taggit',
    'geoposition',
    'djangosecure',
    'easy_thumbnails',
    'embed_video',
    'watson',
    'tinymce',
    'south',
    'adminsortable2',
    'raven.contrib.django.raven_compat',
    'us_ignite.common',
    'us_ignite.profiles',
    'us_ignite.people',
    'us_ignite.apps',
    'us_ignite.awards',
    'us_ignite.hubs',
    'us_ignite.actionclusters',
    'us_ignite.events',
    'us_ignite.organizations',
    'us_ignite.challenges',
    'us_ignite.relay',
    'us_ignite.blog',
    'us_ignite.uploads',
    'us_ignite.resources',
    'us_ignite.maps',
    'us_ignite.sections',
    'us_ignite.news',
    'us_ignite.snippets',
    'us_ignite.mailinglist',
    'us_ignite.visualize',
    'us_ignite.testbeds',
    'us_ignite.globalcityteams',
    'us_ignite.smart_gigabit_communities',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'heroku': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['heroku'],
            'level': 'ERROR',
            'propagate': True,
        },
        'us_ignite.common': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

# Storage settings, filesystem by default:
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Message storage:
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# Email settings:
EMAIL_SUBJECT_PREFIX = '[US Ignite] '
DEFAULT_FROM_EMAIL = 'info@us-ignite.org'
SERVER_EMAIL = 'info@us-ignite.org'

ALLOWED_HOSTS = [
    'local-us-ignite.org',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cookie configuration:
SESSION_COOKIE_HTTPONLY = True
# Avoid embeding the app in an iframe X-Frame-Options:
SECURE_FRAME_DENY = True
# Browser should not guess content-type:
SECURE_CONTENT_TYPE_NOSNIFF = True
# Enable browser XSS protections:
SECURE_BROWSER_XSS_FILTER = True


# Account settings:
ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_REDIRECT_URL = '/dashboard/'
LOGIN_REDIRECT_URL_FAILURE = '/'
LOGOUT_REDIRECT_URL = '/'

# Paginator:
PAGINATOR_PAGE_SIZE = 24

# Uplaoded file restrictions:
MAX_UPLOAD_SIZE = int(1024 * 1024 * 5)   # 5MB

DATETIME_INPUT_FORMATS = (
    '%Y-%m-%d %H:%M:%S',    # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
    '%Y-%m-%d',              # '2006-10-25'
    '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
    '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
    '%m/%d/%Y',              # '10/25/2006'
    '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
    '%m/%d/%y %H:%M',        # '10/25/06 14:30'
    '%m/%d/%y',
)

# Thumbnail format:
THUMBNAIL_EXTENSION = 'png'
THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE

# WP
WP_URL = 'http://us-ignite-wp.herokuapp.com'
WP_EMAIL = ''

# TinyMCE configuration:
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'advanced',
    'theme_advanced_toolbar_location': 'top',
    'plugins': 'table,paste',
    'theme_advanced_buttons1': (',bold,italic,underline,'
                                '|,formatselect,|,bullist,numlist,|,undo,redo,'
                                '|,link,unlink,anchor|,tablecontrols,'),
    'theme_advanced_buttons2': "bullist,numlist,|,outdent,indent,blockquote,hr,|,link,unlink,anchor,image,justifyleft,justifycenter,justifyright,justifyfull|,code,removeformat,cleanup",
    'theme_advanced_blockformats': 'p,h2,h3,h4',
    'forced_root_block': 'p',
    'custom_undo_redo_levels': 20,
    'cleanup_on_startup': True,
    'relative_urls': False,
}
TINYMCE_SPELLCHECKER = False
TINYMCE_COMPRESSOR = False
TINYMCE_FILEBROWSER = False

# Production flag:
IS_PRODUCTION = True

# Asset compressor
COMPRESS_OUTPUT_DIR = ''

GOOGLE_ANALYTICS_ID = 'UA-40470323-1'

IGNITE_MANAGERS = [
    'info@us-ignite.org',
    'jennifer.mott@us-ignite.org',
]

"""
MAILCHIMP_API_KEY = 'set in local.py and production.py'
MAILCHIMP_LIST = 'set in local.py and production.py'

MAILCHIMP_GCTC_API_KEY = 'set in local.py and production.py'
MAILCHIMP_GCTC_LIST = 'set in local.py and production.py'
"""


