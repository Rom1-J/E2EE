from django import template
from rich import inspect

register = template.Library()


@register.filter(name="inspect")
def _inspect(value):
    inspect(value, all=True)

    return value
