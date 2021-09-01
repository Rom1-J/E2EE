import random
from django import template

register = template.Library()


@register.simple_tag
def random_int(a, b=None):
    return random.randint(a, b or 0)


@register.simple_tag
def random_bool():
    return random.choice([True, False])
