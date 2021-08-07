from django import template
from rich import inspect

register = template.Library()


@register.filter
def debug(values):
    inspect(values, all=True)
    return values
