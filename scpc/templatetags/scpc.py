
import os
import math
import urllib.parse
from django import template
from django.template.defaultfilters import stringfilter

from scpc.models import FooterSnippet

_google_api_url = 'https://maps.googleapis.com/maps/api/staticmap'
_google_api_key = os.getenv('GOOGLE_API_KEY')

_googls_maps_default_zoom = 12
_google_maps_styles = [
    # Unencoded values for the `style` query string parameter
    'feature:administrative|element:labels.text.fill|color:0x6195a0',
    'feature:administrative.province|element:geometry.stroke|visibility:off',
    'feature:landscape|element:geometry|color:0xf5f5f2|saturation:0|lightness:0|gamma:1',
    'feature:landscape.man_made|lightness:-5', 'feature:landscape.natural.terrain|visibility:off',
    'feature:poi|visibility:off',
    'feature:poi.park|element:geometry.fill|color:0xbae5ce|visibility:on',
    'feature:road|saturation:-100|lightness:45|visibility:simplified',
    'feature:road.arterial|element:labels.icon|visibility:off',
    'feature:road.arterial|element:labels.text.fill|color:0x787878',
    'feature:road.highway|visibility:simplified',
    'feature:road.highway|element:geometry.fill|color:0xfac9a9|visibility:simplified',
    'feature:road.highway|element:labels.text|color:0x4e4e4e',
    'feature:transit|visibility:simplified',
    'feature:transit.station.airport|element:labels.icon|hue:0x0a00ff|saturation:-77|lightness:0|gamma:0.57',
    'feature:transit.station.rail|element:labels.icon|hue:0xff6c00|saturation:-68|lightness:4|gamma:0.75',
    'feature:transit.station.rail|element:labels.text.fill|color:0x43321e',
    'feature:water|color:0xeaf6f8|visibility:on',
    'feature:water|element:geometry.fill|color:0xc7eced',
    'feature:water|element:labels.text.fill|saturation:-53|lightness:-49|gamma:0.79',
]


register = template.Library()


@register.inclusion_tag('scpc/tags/nav_items.html', takes_context=True)
def nav_items(context, current_page, root_page=None):
    if not root_page:
        root_page = context['request'].site.root_page

    menu_pages = _query_children(root_page)

    for menu_page in menu_pages:
        menu_page.show_dropdown = _query_children(menu_page).exists()

        # We don't directly check if current_page is None since the template
        # engine can pass an empty string to current_page if the variable
        # passed as calling_page does not exist.
        menu_page.active = (
            current_page.path.startswith(menu_page.path) if current_page else False
        )

        if current_page.path.startswith(menu_page.path):
            menu_page.active = True

    return {
        'current_page': current_page,
        'menu_pages': menu_pages,
        'request': context['request'],  # propagate
    }


@register.inclusion_tag('scpc/tags/footer.html', takes_context=True)
def footer(context):
    footer = FooterSnippet.objects.first()

    return {
        'contact_info': footer.contact_info if footer else None,
        'request': context['request'],  # propagate
    }


@register.inclusion_tag('scpc/tags/static_map.html')
def static_map(query, latitude=None, longitude=None, zoom=None, width=100, height=100):
    center = query

    if latitude and longitude:
        # Allow for specifying exact coordinates for the static map. Note that
        # the query argument will still be used for the map URL because a query
        # is the only way we can get Google Maps to display a marker.
        center = '{},{}'.format(latitude, longitude)

    params = {
        'key': _google_api_key,
        'center': center,
        'zoom': zoom if zoom else _googls_maps_default_zoom,
        'size': '{}x{}'.format(width, height),
        'style': _google_maps_styles,
    }

    query_string = urllib.parse.urlencode(params, doseq=True)
    url = '{}?{}'.format(_google_api_url, query_string)

    return {
        'url': url,
        'query': query,
    }


@register.simple_tag(name='aos')
def animation_name(name, alignment):
    if name:
        return name

    by_alignment = {
        'left': 'fade-left',
        'right': 'fade-right',
        'default': 'fade-up',
    }
    return by_alignment[alignment if alignment else 'default']


def _query_children(page):
    return page.get_children().live().in_menu()


# Utility Tags and Filters


class ShrinkwrapNode(template.Node):
    """Remove all redundant whitespace from a rendered :class:`NodeList`."""
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        return ' '.join(output.split())  # Splits on one or more whitespace characters


# noinspection PyUnusedLocal
@register.tag
def shrinkwrap(parser, token):
    """
    The ``{% shrinkwrap %} tag removes all superfluous whitespace rendered within it.
    This is convenient when using multiple lines of tags to produce content which
    should not contain newlines or extra whitespace. For example::

        class="{% shrinkwrap %}
               {% if something %}foo{% endif %}
               {% if another_thing %}bar{% endif %}
               {% elif last_thing %}baz{% endif %}
               {% endif %}
               {% endshrinkwrap %}"

    Assuming ``something`` and ``another_thing`` evaluate to True, this would render::

        class="foo bar"

    """
    nodelist = parser.parse(('endshrinkwrap',))
    parser.delete_first_token()  # Consume end tag
    return ShrinkwrapNode(nodelist)


@register.filter
def partition(query_set, group_count):
    """
    Partitions any sequence (or more specifically, any :class:`QuerySet`) into a number
    of smaller sequences each of size ``group_count``. The final sequence is guaranteed
    to contain at least 1 item but may not contain ``group_count`` items depending on
    the size of the original sequence.

    For example, if foo evaluates to ``[1, 2, 3, 4, 5]``, ``{% foo|partition:3 %}`` would
    evaluate to ``[[1, 2], [3, 4], [5]]``.
    """
    results = query_set.all()
    result_count = query_set.count()

    group_size = int(math.ceil(result_count / group_count))

    # Group the results ``QuerySet`` into equally-sliced QuerySets according to ``group_count``.
    # The last QuerySet in this list may or may not be of equal size. Note that the following
    # expression returns a list of _unevaluated_ QuerySets so as not to query the entire table
    # into memory.
    return [results[i:i + group_size] for i in range(0, result_count, group_size)]


@register.filter()
@stringfilter
def friendly_type(block_type):
    """
    Format a `block_type` name (as in the first item of a :class:`StreamField` tuple)
    as a view-friendly name, e.g. for use as a CSS class name.
    """
    return block_type.replace('_', '-')
