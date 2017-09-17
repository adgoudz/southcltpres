# -*- coding: utf-8 -*-
import aldryn_addons.settings

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
])

MIDDLEWARE_CLASSES.extend([

])

# Wagtail settings
WAGTAIL_ENABLE_UPDATE_CHECK = True

# Django settings
USE_TZ = True
