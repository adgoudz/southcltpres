from django.core.validators import RegexValidator
from django.db import models
from django.forms import widgets
from django.utils.translation import ugettext_lazy
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel, FieldRowPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.blocks import CharBlock
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet


# Stream Blocks


class LocationBlock(blocks.StructBlock):
    """A container similar to :class`TextBlock` which also includes maps, addresses, etc."""
    contact_info = SnippetChooserBlock(target_model='scpc.AddressBookSnippet')
    time = blocks.CharBlock(required=True, max_length=25)
    content = blocks.RichTextBlock(required=True)

    class Meta:
        icon = 'site'
        template = 'scpc/blocks/location.html'


class ContentBlock(blocks.StructBlock):
    """The primary container for generic page content."""
    image = ImageChooserBlock(required=False)
    header = blocks.CharBlock(max_length=32, required=False)
    content = blocks.RichTextBlock()

    class Meta:
        icon = 'form'
        template = 'scpc/blocks/section.html'


class BioBlock(ContentBlock):

    class Meta:
        icon = 'user'


# Root Pages


class SectionedPage(Page):
    """Abstract base class for pages containing :class:`SectionBlock`."""
    sections = StreamField(
        [('text', ContentBlock())],
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
            ('location', LocationBlock()),
            ('text', ContentBlock()),
            ('bio', BioBlock()),
            ('divider', CharBlock(
                icon='horizontalrule',
                required=True,
                max_length=25,
                template='scpc/blocks/divider.html')),
            ('verse', SnippetChooserBlock(
                template='scpc/blocks/verse.html',
                target_model='scpc.VerseSnippet'))
        ],
        blank=True
    )

    subtitle = models.CharField(max_length=35)
    introduction = RichTextField(max_length=750)

    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel('subtitle', classname='title'),
                FieldPanel('introduction', classname='full'),
            ],
            heading='Header'
        ),
        StreamFieldPanel('sections'),
    ]

    class Meta:
        verbose_name = 'homepage'


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
    hero_align = models.CharField(
        verbose_name='Alignment',
        max_length=6,
        choices=(
            ('top', 'Top'),
            ('middle', 'Middle'),
            ('bottom', 'Bottom'),
        ),
        default='middle',
        help_text='Aligns the image vertically',
    )
    hero_y = models.PositiveSmallIntegerField(
        verbose_name='Y',
        default=50,
        help_text='The vertical position to align to the middle of the container (middle alignment only)',
    )

    menu_title = models.CharField(
        max_length=12,
        null=True,
        blank=True,
        help_text='An alternate page title to be used in automatically generated menus'
    )

    content_panels = [
        MultiFieldPanel(
            [
                ImageChooserPanel('hero_image'),
                FieldPanel('hero_align', widget=widgets.RadioSelect),
                FieldPanel('hero_y'),
            ],
            heading="Hero"
        )
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


@register_snippet
class AddressBookSnippet(models.Model):

    facebook_url = models.URLField(verbose_name='Facebook')
    twitter_url = models.URLField(verbose_name='Twitter')
    instagram_url = models.URLField(verbose_name='Instagram')

    location_name = models.CharField(verbose_name='Name', max_length=22)
    location_street = models.CharField(verbose_name='Street', max_length=22)
    location_city = models.CharField(verbose_name='City, State, Zip', max_length=22)
    directions_url = models.URLField(verbose_name='Google Maps', max_length=350)

    mailing_name = models.CharField(verbose_name='Name', max_length=22, null=True, blank=True)
    mailing_street = models.CharField(null=True, verbose_name='Street', max_length=22)
    mailing_city = models.CharField(null=True, verbose_name='City, State, Zip', max_length=22)

    email = models.EmailField(null=True)

    phone_regex = RegexValidator(regex=r'^(\+1 )?[()0-9-. ]{9,20}$',
                                 message="Phone numbers should contain only digits and optional delimiters.")
    phone_number = models.CharField(verbose_name='Phone', validators=[phone_regex], max_length=23, null=True, blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('location_name'),
                FieldPanel('location_street'),
                FieldPanel('location_city'),
                FieldPanel('directions_url'),
            ],
            heading='Service Address'
        ),
        MultiFieldPanel(
            [
                FieldPanel('mailing_name'),
                FieldPanel('mailing_street'),
                FieldPanel('mailing_city'),
            ],
            heading='Mailing Address'
        ),
        MultiFieldPanel(
            [
                FieldPanel('facebook_url'),
                FieldPanel('twitter_url'),
                FieldPanel('instagram_url'),
            ],
            heading='Social Media'
        ),
        MultiFieldPanel(
            [
                FieldPanel('email'),
                FieldPanel('phone_number'),
            ],
            heading='Other'
        )
    ]

    def __str__(self):
        return 'Default'


@register_snippet
class FooterSnippet(models.Model):

    contact_info = models.ForeignKey(
        'scpc.AddressBookSnippet',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        SnippetChooserPanel('contact_info')
    ]

    def __str__(self):
        return 'Default'
