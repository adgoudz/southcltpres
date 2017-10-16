
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
        menu_page.active = False

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
