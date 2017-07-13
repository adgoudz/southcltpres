# -*- coding: utf-8 -*-
from aldryn_client import forms


class Form(forms.BaseForm):
    wagtail_site_name = forms.CharField(
        'Wagtail Sitename',
        required=True,
        initial='My Example Site',
    )

    def to_settings(self, data, settings):
        settings['INSTALLED_APPS'].extend([
            'wagtail.wagtailforms',
            'wagtail.wagtailredirects',
            'wagtail.wagtailembeds',
            'wagtail.wagtailsites',
            'wagtail.wagtailusers',
            'wagtail.wagtailsnippets',
            'wagtail.wagtaildocs',
            'wagtail.wagtailimages',
            'wagtail.wagtailsearch',
            'wagtail.wagtailadmin',
            'wagtail.wagtailcore',

            'modelcluster',
            'taggit',
        ])
        settings['MIDDLEWARE_CLASSES'].extend([
            'wagtail.wagtailcore.middleware.SiteMiddleware',
            'wagtail.wagtailredirects.middleware.RedirectMiddleware',
        ])
        # admin and cms urls need to be first, since we're overriding the
        # default admin.
        settings['ADDON_URLS_I18N'].insert(
            0,
            'aldryn_wagtail.urls',
        )
        settings['ADDON_URLS_I18N_LAST'] = 'aldryn_wagtail.page_urls'
        settings['WAGTAIL_SITE_NAME'] = data['wagtail_site_name']

        return settings
