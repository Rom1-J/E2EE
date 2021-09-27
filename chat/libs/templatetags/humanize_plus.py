import humanize
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def naturalsize(value: int):
    return humanize.naturalsize(value)


@register.filter
def bold_extension(filename: str):
    frags = filename.split(".")

    extension = frags.pop()

    return mark_safe(f"{'.'.join(frags)}<b>.{extension}</b>")
