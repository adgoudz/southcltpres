from django.db import models
from django.utils.translation import ugettext_lazy
from django.utils.safestring import mark_safe

from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.blocks import StaticBlock
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock
from wagtail.wagtailsnippets.models import register_snippet


# Functions


def _static_label(label):
    return mark_safe('<label style="width: 14%">{label}:</label> '
                     '<p style="font-size: 1.1em; padding-top: 1.2em; padding-bottom: 0.8em;">'
                     'This section cannot be configured.</p>'.format(label=label))


# Stream Blocks


class SectionBlock(blocks.StructBlock):
    """The primary container for generic page content."""
    image = ImageChooserBlock(required=False)
    name = blocks.CharBlock(max_length=32, required=False)
    content = blocks.RichTextBlock()

    class Meta:
        icon = 'form'
        template = 'scpc/blocks/section.html'


# Root Pages


class SectionedPage(Page):
    """Abstract base class for pages containing :class:`SectionBlock`."""
    sections = StreamField(
        [('section', SectionBlock())],
        blank=True
    )
    sections_panel = StreamFieldPanel('sections')

    content_panels = Page.content_panels + [
        sections_panel
    ]

    class Meta:
        abstract = True


class HomePage(Page):
    """The permanent home page for the site."""

    parent_page_types = []
    subpage_types = [
        'scpc.MinistriesPage',
        'scpc.AboutUsPage',
        'scpc.GospelPage',
        'scpc.GivingPage',
    ]

    # Extend `SectionedPage` stream field
    sections = StreamField(
        [
            ('section', SectionBlock()),
            ('map', StaticBlock(icon='site', template='scpc/blocks/map.html', admin_text=_static_label('Map'))),
            ('verse', SnippetChooserBlock(template='scpc/blocks/verse.html', target_model='scpc.VerseSnippet'))
        ],
        blank=True
    )

    subtitle = models.CharField(max_length=35)
    introduction = RichTextField(max_length=750)

    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel('title', classname='title'),
                FieldPanel('subtitle', classname='title'),
                FieldPanel('introduction', classname='full'),
            ],
            heading='Header'
        ),
        StreamFieldPanel('sections'),
    ]

    class Meta:
        verbose_name = 'homepage'


class LandingPage(Page):
    """The home page used to announce the church."""

    location_title = models.CharField(verbose_name='Title', max_length=65, blank=True)
    location_subtitle = models.CharField(verbose_name='Subtitle', max_length=100, blank=True)
    location_content = RichTextField(verbose_name='Content', max_length=750, blank=True)

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


class Subpage(SectionedPage):

    parent_page_types = ['scpc.HomePage']
    subpage_types = []

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    menu_title = models.CharField(
        max_length=12,
        null=True,
        blank=True,
        help_text="An alternate page title to be used in automatically generated menus"
    )

    content_panels = [
        ImageChooserPanel('hero_image')
    ] + SectionedPage.content_panels

    promote_panels = MultiFieldPanel([
        FieldPanel('slug'),
        FieldPanel('seo_title'),
        FieldPanel('show_in_menus'),
        FieldPanel('menu_title'),
        FieldPanel('search_description'),
    ], ugettext_lazy('Common page configuration')),

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


# Snippets


@register_snippet
class VerseSnippet(models.Model):

    passage = models.TextField(max_length=750)
    verse = models.CharField(max_length=25)

    panels = [
        FieldPanel('passage'),
        FieldPanel('verse'),
    ]

    def __str__(self):
        return self.verse

