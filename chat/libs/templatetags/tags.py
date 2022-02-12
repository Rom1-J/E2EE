from django import template
from django.shortcuts import resolve_url
from django.utils.html import format_html

from chat.apps.guilds.features.channels.models import Channel
from chat.apps.guilds.models import Guild

register = template.Library()


@register.simple_tag
def channel_anchor(guild: Guild, channel: Channel, **kwargs):
    return format_html(
        """<a href="{link}" class="uk-link {extra_class}">
                        <span uk-icon="icon: hashtag"></span>
                        <span>{channel_name}</span>
                    </a>""",
        link=resolve_url("guild:channel_details", guild.id, channel.id),
        extra_class=(
            "uk-text-bold"
            if kwargs.get("current", None) == channel.id
            else "uk-text-muted"
        ),
        channel_name=channel.name,
    )
