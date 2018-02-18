# -*- coding: utf-8 -*-

# noinspection PyUnresolvedReferences
from django.conf.urls import url, include
from aldryn_django.utils import i18n_patterns
from django.views.generic import TemplateView
from wagtail.contrib.wagtailsitemaps.views import sitemap

import aldryn_addons.urls


urlpatterns = (
    [
        url('^robots\.txt$', TemplateView.as_view(template_name='scpc/robots.txt', content_type='text/plain')),
        url('^sitemap\.xml$', sitemap),
    ]
    + aldryn_addons.urls.patterns()
    + i18n_patterns(*aldryn_addons.urls.i18n_patterns())  # Must be the last entry!
)
