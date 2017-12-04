import math
from django import template

from scpc.models import FooterSnippet

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
