from django import template
from faker import Faker
from mdgen import MarkdownPostProvider


register = template.Library()
fake = Faker()
fake.add_provider(MarkdownPostProvider)


@register.filter(name="fake")
def do_fake_filter(formatter, args=None):
    """
    call a faker format
    uses:
        {{ 'randomElement'|fake:mylist }}
        {% if 'boolean'|fake:30 %} .. {% endif %}
        {% for word in 'words'|fake:times %}{{ word }}\n{% endfor %}
    """
    cleaned_args = []

    if args:
        for arg in args.split(","):
            cleaned_args.append(int(arg) if arg.isdigit() else arg)

    return getattr(fake, formatter)(*cleaned_args)


@register.filter(name="or_fake")
def do_or_fake_filter(value, formatter):
    """
    call a faker if value is None
    uses:
        {{ myint|or_fake:'randomInt' }}
    """
    return value or getattr(fake, formatter)()


@register.filter
def get_range(value):
    """
      http://djangosnippets.org/snippets/1357/
    Filter - returns a list containing range made from given value
    Usage (in template):
    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>
    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>
    Instead of 3 one may use the variable set in the views
    """
    return range(value)
