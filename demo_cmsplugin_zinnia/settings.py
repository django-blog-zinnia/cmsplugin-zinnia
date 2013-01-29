"""Settings for the cmsplugin_zinnia demo"""
import os

gettext = lambda s: s

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

DATABASES = {'default':
             {'ENGINE': 'django.db.backends.sqlite3',
              'NAME': os.path.join(PROJECT_ROOT, 'demo.db')}
             }

TIME_ZONE = 'Europe/Paris'

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

SECRET_KEY = 'fgh1rzme%sfv3#n+fb7h948yuv3(pt63abhi12_t7e^^5q8dyw'

USE_TZ = True
USE_I18N = True
USE_L10N = True

SITE_ID = 1

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', gettext('English')),
    ('fr', gettext('French')),
    ('de', gettext('German')),
    ('es', gettext('Spanish')),
    ('it', gettext('Italian')),
    ('nl', gettext('Dutch')),
    ('hu', gettext('Hungarian')),
    ('cs', gettext('Czech')),
    ('sk', gettext('Slovak')),
    ('ru', gettext('Russian')),
    ('pl', gettext('Polish')),
    ('eu', gettext('Basque')),
    ('ca', gettext('Catalan')),
    ('tr', gettext('Turkish')),
    ('hr_HR', gettext('Croatian')),
    ('pt_BR', gettext('Brazilian Portuguese')),
    ('fi_FI', gettext('Finnish (Finland)')),
    ('zh_CN', gettext('Simplified Chinese')),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
)

ROOT_URLCONF = 'demo_cmsplugin_zinnia.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'zinnia.context_processors.version',
    'sekizai.context_processors.sekizai',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sitemaps',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.staticfiles',
    'mptt',
    'zinnia',
    'tagging',
    'sekizai',
    'cms',
    'cms.plugins.text',
    'cmsplugin_zinnia',
    'menus',
)

CMS_TEMPLATES = (
    ('cms/page.html', gettext('Default page')),
)

CMS_SEO_FIELDS = True

ZINNIA_ENTRY_BASE_MODEL = 'cmsplugin_zinnia.placeholder.EntryPlaceholder'
