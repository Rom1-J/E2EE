from typing import List, Union

from django import template
from django.contrib.auth import get_user_model

from chat.guilds.features.channels.models import Category, Channel, Message
from chat.guilds.models import Guild

User = get_user_model()
register = template.Library()


@register.filter(name="get_messages_sent")
def get_messages_sent(member: User, guild: Guild):  # type: ignore
    return Message.objects.filter(channel__guild=guild, author=member)


@register.filter(name="show_channels_and_categories")
def show_channels_and_categories(guild: Guild):
    output: List[Union[Category, Channel]] = []

    output.extend(guild.channels.filter(parent=None).all())
    output.extend(guild.categories.all())

    output.sort(key=lambda x: x.position)

    return output


@register.filter(name="show_channels_from_category")
def show_channels_from_category(category: Category):
    output: List[Channel] = []

    output.extend(Channel.objects.filter(parent=category).all())

    output.sort(key=lambda x: x.position)

    return output
