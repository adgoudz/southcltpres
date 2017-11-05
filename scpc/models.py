from django.core.validators import RegexValidator
from django.db import models
from django.forms import widgets
from django.utils.translation import ugettext_lazy
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel, InlinePanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet


# Stream Blocks


class ContentBlock(blocks.StructBlock):
    """The primary container for generic page content."""
    image = ImageChooserBlock(required=False)
    header = blocks.CharBlock(max_length=32, required=False)
    subheader = blocks.CharBlock(max_length=32, required=False)
    content = blocks.RichTextBlock()

    class Meta:
        icon = 'form'
        template = 'scpc/blocks/content.html'


class LocationBlock(blocks.StructBlock):
    """A container similar to :class`TextBlock` which also includes maps, addresses, etc."""
    contact_info = SnippetChooserBlock(target_model='scpc.AddressBookSnippet')
    time = blocks.CharBlock(required=True, max_length=25)
    content = blocks.RichTextBlock(required=True)

    class Meta:
        icon = 'site'
        template = 'scpc/blocks/location.html'


class DividerBlock(blocks.CharBlock):
    """A reusable :class:`CharBlock` for page dividers."""

    def __init__(self, required=True, help_text=None, max_length=25, min_length=None, **kwargs):
        kwargs['icon'] = 'horizontalrule'
        kwargs['template'] = 'scpc/blocks/divider.html'
        super(DividerBlock, self).__init__(required, help_text, max_length, min_length, **kwargs)


# Inline Models


class BaseProfile(models.Model):
    """Staff profiles which may or may not contain a bio and contact information."""
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True, blank=True)

    name = models.CharField(max_length=32)
    title = models.CharField(max_length=32)

    email = models.EmailField(null=True, blank=True)

    class Meta:
        abstract = True


class LeadershipProfile(BaseProfile):
    twitter_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)

    bio = RichTextField(null=True, blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('name'),
        FieldPanel('title'),
        FieldPanel('bio', classname='full'),
        MultiFieldPanel(
            [
                FieldPanel('email'),
                FieldPanel('twitter_url'),
                FieldPanel('facebook_url'),
                FieldPanel('instagram_url'),
            ],
            heading='Contact Info',
            classname='collapsible collapsed',
        )
    ]

    class Meta:
        abstract = True


class StaffProfile(BaseProfile):
    panels = [
        ImageChooserPanel('image'),
        FieldPanel('name'),
        FieldPanel('title'),
        FieldPanel('email'),
    ]

    class Meta:
        abstract = True


# Root Pages


class HomePage(Page):
    """The permanent home page for the site."""
    parent_page_types = []

    # Extend `SectionedPage` stream field
    content = StreamField(
        [
            ('location', LocationBlock()),
            ('text', ContentBlock()),
            ('verse', SnippetChooserBlock(
                target_model='scpc.VerseSnippet',
                template='scpc/blocks/verse.html')),
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
        StreamFieldPanel('content'),
    ]

    class Meta:
        verbose_name = 'homepage'


# Subpages


class Subpage(Page):

    parent_page_types = ['scpc.HomePage']
    subpage_types = []

    menu_title = models.CharField(
        max_length=12,
        null=True,
        blank=True,
        help_text='An alternate page title to be used in automatically generated menus'
    )

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

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                ImageChooserPanel('hero_image'),
                FieldPanel('hero_align', widget=widgets.RadioSelect),
                FieldPanel('hero_y'),
            ],
            heading="Hero"
        ),
    ]

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

    sections = StreamField(
        [
            ('text', ContentBlock()),
        ],
        blank=True
    )

    content_panels = Subpage.content_panels + [
        StreamFieldPanel('sections'),
    ]


class AboutUsPage(Subpage):

    content = StreamField(
        [
            ('text', ContentBlock()),
            ('divider', DividerBlock()),

        ],
        blank=True
    )

    content_panels = Subpage.content_panels + [
        StreamFieldPanel('content'),
        InlinePanel('leadership', label='Leadership'),
        InlinePanel('staff', label='Staff'),
    ]


class AboutUsLeader(Orderable, LeadershipProfile):
    page = ParentalKey('scpc.AboutUsPage', related_name='leadership')


class AboutUsStaff(Orderable, StaffProfile):
    page = ParentalKey('scpc.AboutUsPage', related_name='staff')


class GospelPage(Subpage):

    sections = StreamField(
        [
            ('text', ContentBlock()),
        ],
        blank=True
    )

    content_panels = Subpage.content_panels + [
        StreamFieldPanel('sections'),
    ]


class GivingPage(Subpage):

    sections = StreamField(
        [
            ('text', ContentBlock()),
        ],
        blank=True
    )

    content_panels = Subpage.content_panels + [
        StreamFieldPanel('sections'),
    ]


class StyleGuidePage(Page):
    """A subpage for showcasing and testing all page elements."""
    parent_page_types = ['scpc.HomePage']
    subpage_types = []

    sections = StreamField(
        [
            ('text', ContentBlock()),
        ],
        blank=True
    )

    custom = StreamField(
        [
            ('location', LocationBlock()),
            ('divider', blocks.CharBlock(
                icon='horizontalrule',
                required=True,
                max_length=25,
                template='scpc/blocks/divider.html')),
            ('verse', SnippetChooserBlock(
                target_model='scpc.VerseSnippet',
                template='scpc/blocks/verse.html')),
        ],
        blank=True
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel('sections'),
        StreamFieldPanel('custom'),
    ]


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
