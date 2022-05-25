from django import template

register = template.Library()


@register.filter
def replace(value, arg: str):
    if len(arg.split('|')) != 2:
        return value

    what, to = arg.split('|')
    return str(value).replace(what, to)
