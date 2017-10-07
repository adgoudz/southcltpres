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
    'webpack_loader',
    'wagtail.contrib.wagtailstyleguide',
])

MIDDLEWARE_CLASSES.extend([

])

# Wagtail settings
WAGTAIL_ENABLE_UPDATE_CHECK = True

# Django settings
USE_TZ = True

# Webpack settings
WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'bundles/',  # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR, 'static/webpack-stats.json'),
    }
}
