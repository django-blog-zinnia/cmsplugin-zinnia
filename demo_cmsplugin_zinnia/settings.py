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

SECRET_KEY = 'fgh1rzme%sfv3#n+fb7h948yuv3(pt63abhi12_t7e^^5q8dyw'

USE_TZ = True
USE_I18N = True
USE_L10N = True

SITE_ID = 1

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', gettext('English')),
    ('fr', gettext('French')),
)

MIDDLEWARE_CLASSES = (
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
)

ROOT_URLCONF = 'demo_cmsplugin_zinnia.urls'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'zinnia.context_processors.version',
                'sekizai.context_processors.sekizai',
                'cms.context_processors.cms_settings',
            ],
        },
    },
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sitemaps',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'djangocms_admin_style',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django_comments',
    'mptt',
    'zinnia',
    'tagging',
    'sekizai',
    'treebeard',
    'djangocms_text_ckeditor',
    'cms',
    'cmsplugin_zinnia',
    'menus',
)

CMS_TEMPLATES = (
    ('cms/page.html', gettext('Default page')),
)

ZINNIA_ENTRY_BASE_MODEL = 'cmsplugin_zinnia.placeholder.EntryPlaceholder'

MIGRATION_MODULES = {
    'zinnia': 'demo_cmsplugin_zinnia.migrations.zinnia',
}
