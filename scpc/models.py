from turtledemo.chaos import h

from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page


# Root Pages


class HomePage(Page):
    """The root page for the site."""

    class Meta:
        verbose_name = 'homepage'


class LandingPage(Page):
    """The home page used to announce the church."""

    location_title = models.CharField(verbose_name='Title', max_length=65, blank=True)
    location_subtitle = models.CharField(verbose_name='Subtitle', max_length=100, blank=True)
    location_content = RichTextField(verbose_name='Content', max_length=500, blank=True)

    address_name = models.CharField(verbose_name='Name', max_length=22, blank=True)
    address_street = models.CharField(verbose_name='Street', max_length=22, blank=True)
    address_city = models.CharField(verbose_name='City, State, Zip', max_length=22, blank=True)
    directions_url = models.URLField(default='http://www.google.com/maps', max_length=350)

    # TODO Move these to a snippet or a footer model
    facebook_url = models.URLField(verbose_name='Facebook', default='http://www.facebook.com')
    twitter_url = models.URLField(verbose_name='Twitter', default='http://www.twitter.com')
    instagram_url = models.URLField(verbose_name='Instagram', default='http://www.instagram.com')

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('location_title', classname='title'),
                FieldPanel('location_subtitle', classname='title'),
                FieldPanel('location_content', classname='full'),
            ],
            heading='Location'
        ),
        MultiFieldPanel(
            [
                FieldPanel('address_name'),
                FieldPanel('address_street'),
                FieldPanel('address_city'),
                FieldPanel('directions_url'),
            ],
            heading='Address'
        ),
        MultiFieldPanel(
            [
                FieldPanel('facebook_url'),
                FieldPanel('twitter_url'),
                FieldPanel('instagram_url'),
            ],
            heading='Social Media URLs'
        )
    ]

    parent_page_types = []
    subpage_types = []


# Subpages


class Subpage(Page):

    parent_page_types = ['scpc.HomePage']
    subpage_types = []

    class Meta:
        abstract = True


class MinistriesPage(Subpage):
    pass


class AboutUsPage(Subpage):
    pass


class GospelPage(Subpage):
    pass


class GivingPage(Subpage):
    pass


class ContactUsPage(Subpage):
    pass
