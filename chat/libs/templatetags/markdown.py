from django import template

register = template.Library()


@register.filter(name="markdown")
def markdown(content):
    return content
