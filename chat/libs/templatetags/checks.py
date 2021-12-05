from importlib import import_module

from django import template

register = template.Library()


@register.filter(name="isinstance")
def _isinstance(value, class_str):
    split = class_str.split(".")

    return isinstance(
        value, getattr(import_module(".".join(split[:-1])), split[-1])
    )
