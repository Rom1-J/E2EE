import random
import uuid

from django import template
from faker import Faker
from mdgen import MarkdownPostProvider

fake = Faker()
fake.add_provider(MarkdownPostProvider)
register = template.Library()


@register.simple_tag
def random_int(a, b=None):
    return random.randint(a, b or 0)


@register.simple_tag
def random_bool():
    return random.choice([True, False])


@register.simple_tag
def random_uuid():
    return str(uuid.uuid4())


@register.simple_tag
def random_post():
    return fake.post()
