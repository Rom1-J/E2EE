import datetime

from django import template
from django.utils.timezone import utc
from django.utils.translation import gettext as _

register = template.Library()


@register.filter
def good_morning(username: str):
    hour = int(datetime.datetime.utcnow().replace(tzinfo=utc).strftime("%H"))

    if hour >= 22 or hour < 6:
        return _("Good evening {username}").format(username=username)

    if hour >= 12:
        return _("Good afternoon {username}").format(username=username)

    return _("Good morning {username}").format(username=username)
