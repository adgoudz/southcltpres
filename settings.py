# -*- coding: utf-8 -*-
import os

import aldryn_addons.settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEBUG = os.getenv('DEBUG', False)

INSTALLED_ADDONS = [
    # <INSTALLED_ADDONS>  # Warning: text inside the INSTALLED_ADDONS tags is auto-generated. Manual changes will be overwritten.
    'aldryn-addons',
    'aldryn-django',
    'aldryn-sso',
    'aldryn-devsync',
    'aldryn-wagtail',
    # </INSTALLED_ADDONS>
]

aldryn_addons.settings.load(locals())

INSTALLED_APPS.extend([
    'scpc',

    # Static File Management
    'webpack_loader',

    # Template Utilities
    'mathfilters',

    # Wagtail Contrib
    'wagtail.contrib.wagtailstyleguide',
    "wagtail.contrib.wagtailsitemaps",
])

TEMPLATES[0]['OPTIONS']['context_processors'].append(
    'scpc.context_processors.env.export'
)

# Wagtail settings

WAGTAIL_ENABLE_UPDATE_CHECK = False
WAGTAIL_PASSWORD_RESET_ENABLED = False
WAGTAILADMIN_NOTIFICATION_USE_HTML = True

# Django settings

USE_TZ = True

# The following email settings are set in test/production environments via the EMAIL_URL
# environment variable (via dj-email-url). They can be uncommented here to test email from
# local machines.
# EMAIL_HOST = 'smtp-relay.gmail.com'
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

SERVER_EMAIL = 'webmaster@southcltpres.org'
DEFAULT_FROM_EMAIL = SERVER_EMAIL

# Webpack settings

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'bundles/',  # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR, 'static/webpack-stats.json'),
    }
}
