from typing import List, Union

from django import template
from django.contrib.auth import get_user_model

from chat.apps.guilds.features.channels.models import (
    Category,
    Channel,
    Message,
)
from chat.apps.guilds.models import Guild
from chat.apps.users.models import UserSettings

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


@register.simple_tag(name="collapsed_category")
def collapsed_category(category: Category, member: User):  # type: ignore
    if hasattr(member, "settings") and member.settings:  # type: ignore
        user_settings: UserSettings = member.settings  # type: ignore

        return user_settings.collapsed_categories.filter(
            id=category.id
        ).exists()

    return False
