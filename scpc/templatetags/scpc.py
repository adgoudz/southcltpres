
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


# Utility Tags


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
    nodelist = parser.parse(('endshrinkwrap',))
    parser.delete_first_token()  # Consume end tag
    return ShrinkwrapNode(nodelist)
