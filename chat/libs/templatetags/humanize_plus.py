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

    return mark_safe(
        f"<span>{'.'.join(frags)}"
        f"<b class='uk-text-warning uk-text-bold'>"
        f".{extension}"
        f"</b>"
        f"</span>"
    )
