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

from . import utils

_header_help_text = utils.join_lines(
    '''
    The site-wide style for headers is to use sentence case (not title case).
    Try not to capitalize words unless you'd normally do so in a sentence.
    '''
)
_svg_help_text = utils.join_lines(
    '''
    For icon images we use the SVG format and SVGs cannot be uploaded here.
    This path must refer to an SVG which already exists. Modifying the icon
    requires changing the raw file externally from Wagtail.
    '''
)
_map_query_help_text = utils.join_lines(
    '''
    This is used both for creating a static map image and for auto-filling 
    the search box when this static map is clicked. If Google Maps is unable 
    to reverse-geocode this query to a single location, latitude and longitude 
    coordinates can be provided below to center the static map.
    '''
)
_map_zoom_help_text = utils.join_lines(
    '''
    See https://developers.google.com/maps/documentation/static-maps/intro
    #Zoomlevels. The default zoom is 12.
    '''
)


# Stream Blocks


class ContentBlock(blocks.StructBlock):
    """The primary container for generic page content."""
    image = ImageChooserBlock(required=False)
    header = blocks.CharBlock(max_length=32, required=False, help_text=_header_help_text)
    subheader = blocks.CharBlock(max_length=32, required=False)
    content = blocks.RichTextBlock()

    class Meta:
        icon = 'form'
        template = 'scpc/blocks/content.html'


class LocationBlock(blocks.StructBlock):
    """A container for content describing the church's location."""
    contact_info = SnippetChooserBlock(target_model='scpc.AddressBookSnippet')
    time = blocks.CharBlock(max_length=25)
    content = blocks.RichTextBlock()

    class Meta:
        icon = 'site'
        template = 'scpc/blocks/location.html'


class LifeGroupBlock(blocks.StructBlock):
    """A container for describing an individual life group. Used by :class:`LifeGroupsBlock`."""
    day = blocks.ChoiceBlock([
        ('Sundays', 'Sundays'),
        ('Mondays', 'Mondays'),
        ('Tuesdays', 'Tuesdays'),
        ('Wednesdays', 'Wednesdays'),
        ('Thursdays', 'Thursdays'),
        ('Fridays', 'Fridays'),
        ('Saturdays', 'Saturdays'),
    ], default='Sundays')

    time = blocks.CharBlock(
        max_length=12,
        help_text='Try to stick to the format "HH-HHpm".')
    region = blocks.CharBlock(
        max_length=25,
        help_text='This should be a commonly-recognized area of Charlotte.')
    location = blocks.CharBlock(
        max_length=32,
        help_text='This should be a nearby intersection or well-known neighborhood.')

    childcare_policy = blocks.TextBlock()

    map = blocks.StructBlock([
        ('query', blocks.CharBlock(help_text=_map_query_help_text)),
        ('zoom', blocks.IntegerBlock(required=False, min_value=1, max_value=20, help_text=_map_zoom_help_text)),
        ('latitude', blocks.CharBlock(required=False, label='Lat.')),
        ('longitude', blocks.CharBlock(required=False, label='Long.')),
    ], template='scpc/blocks/lifegroups/map.html')

    class Meta:
        template = 'scpc/blocks/lifegroups/lifegroup.html'


class LifeGroupsBlock(ContentBlock):
    """A container for content describing the life groups ministry."""
    groups = blocks.ListBlock(LifeGroupBlock())

    class Meta:
        label = 'Life Groups'
        template = 'scpc/blocks/lifegroups.html'


class DividerBlock(blocks.CharBlock):
    """A reusable :class:`CharBlock` for page dividers."""

    def __init__(self, required=True, help_text=None, max_length=25, min_length=None, **kwargs):
        kwargs['icon'] = 'horizontalrule'
        kwargs['template'] = 'scpc/blocks/divider.html'
        super(DividerBlock, self).__init__(required, help_text, max_length, min_length, **kwargs)


# Inline Models


class Vision(models.Model):
    """A single vision for the church which comprises the overall vision statement."""
    image_src = models.CharField(max_length=50, verbose_name='Icon Path', help_text=_svg_help_text)
    header = models.CharField(max_length=25)
    content = models.TextField(max_length=200)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('image_src'),
            ],
            'Icon',
            classname='collapsible collapsed',
        ),
        FieldPanel('header'),
        FieldPanel('content'),
    ]

    class Meta:
        abstract = True


class BaseProfile(models.Model):
    """Staff profiles which may or may not contain a bio and contact information."""
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True, blank=True)
    name = models.CharField(max_length=32)
    title = models.CharField(max_length=32)

    email = models.EmailField(null=True, blank=True)

    class Meta:
        abstract = True


class LeadershipProfile(BaseProfile):
    """A large profile for pastors, elders, etc."""
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
    """A smaller profile for staff members."""
    panels = [
        ImageChooserPanel('image'),
        FieldPanel('name'),
        FieldPanel('title'),
        FieldPanel('email'),
    ]

    class Meta:
        abstract = True


class Doctrine(models.Model):
    """A single doctrine in the summary of the church's theology."""
    header = models.CharField(max_length=25)
    content = models.TextField(max_length=200)

    panels = [
        FieldPanel('header'),
        FieldPanel('content'),
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
    introduction = RichTextField()

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
    """An abstract base `Page` for all children of :class:`HomePage`."""
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

    content = StreamField(
        [
            ('children', ContentBlock()),
            ('youth', ContentBlock()),
            ('life_groups', LifeGroupsBlock()),
        ],
    )

    content_panels = Subpage.content_panels + [
        StreamFieldPanel('content'),
    ]


class AboutUsPage(Subpage):

    introduction = models.TextField()
    vision_header = models.CharField(max_length=32)
    vision_intro = RichTextField()
    profiles_header = models.CharField(verbose_name='Divider', max_length=25)
    staff_header = models.CharField(max_length=25)

    content_panels = Subpage.content_panels + [
        FieldPanel('introduction', classname='full'),
        FieldPanel('vision_header'),
        FieldPanel('vision_intro'),
        InlinePanel('vision_statement', label='Hopes'),
        FieldPanel('profiles_header'),
        InlinePanel('leadership', label='Leadership'),
        FieldPanel('staff_header'),
        InlinePanel('staff', label='Staff'),
    ]


class AboutUsVision(Orderable, Vision):
    page = ParentalKey('scpc.AboutUsPage', related_name='vision_statement')


class AboutUsLeader(Orderable, LeadershipProfile):
    page = ParentalKey('scpc.AboutUsPage', related_name='leadership')


class AboutUsStaff(Orderable, StaffProfile):
    page = ParentalKey('scpc.AboutUsPage', related_name='staff')


class BeliefsPage(Subpage):

    introduction = models.TextField()
    gospel_header = models.CharField(max_length=25)
    gospel_content = RichTextField()
    doctrines_header = models.CharField(max_length=32)
    doctrines_intro = RichTextField()

    content_panels = Subpage.content_panels + [
        FieldPanel('introduction', classname='full'),
        FieldPanel('gospel_header'),
        FieldPanel('gospel_content'),
        FieldPanel('doctrines_header'),
        FieldPanel('doctrines_intro'),
        InlinePanel('doctrines', label='Doctrines'),
    ]


class BeliefsDoctrine(Orderable, Doctrine):
    page = ParentalKey('scpc.BeliefsPage', related_name='doctrines')


class GivingPage(Subpage):

    introduction = RichTextField()
    giving_content = RichTextField()
    online_link_name = models.CharField(max_length=15)
    online_link_url = models.URLField()
    mail_header = models.CharField(max_length=32)

    contact_info = models.ForeignKey(
        'scpc.AddressBookSnippet',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = Subpage.content_panels + [
        FieldPanel('introduction'),
        FieldPanel('giving_content'),
        MultiFieldPanel(
            [
                FieldPanel('online_link_name'),
                FieldPanel('online_link_url'),
                FieldPanel('mail_header'),
                SnippetChooserPanel('contact_info'),
            ],
            heading='Giving Details',
        ),
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
            ('life_groups', LifeGroupsBlock()),
            ('divider', DividerBlock()),
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

    location_name = models.CharField(verbose_name='Name', max_length=50)
    location_street = models.CharField(verbose_name='Street', max_length=22)
    location_city = models.CharField(verbose_name='City, State, Zip', max_length=22)
    directions_url = models.URLField(verbose_name='Google Maps')

    mailing_name = models.CharField(verbose_name='Name', max_length=50, null=True, blank=True)
    mailing_street = models.CharField(verbose_name='Street', max_length=22, null=True, blank=True)
    mailing_city = models.CharField(verbose_name='City, State, Zip', max_length=22, null=True, blank=True)

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
