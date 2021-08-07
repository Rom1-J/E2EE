from django import template

register = template.Library()


@register.filter
def abs_url(path: str):
    return "http://127.0.0.1:3000" + path
