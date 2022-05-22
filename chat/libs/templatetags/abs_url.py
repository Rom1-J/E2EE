from django import template

register = template.Library()


@register.filter
def abs_url(path: str):
    return "https://c3e.gnous.eu" + path
