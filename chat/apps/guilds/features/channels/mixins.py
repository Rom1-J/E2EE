from django.shortcuts import redirect

from ...mixins import IsInGuildMixin
from ...models import Guild


def chan_exists(request, *args, **kwargs):
    guild_id: str = str(kwargs.pop("guild_id", ""))
    channel_id: str = str(kwargs.pop("channel_id", ""))

    if guild_id and channel_id:
        channel = Guild.objects.get(
            id=guild_id,
            members__in=[request.user],
        ).channels.get(id__exact=channel_id)

        return channel or redirect("guild:guild_details", guild_id=guild_id)

    return False


class ChanExistsMixin(IsInGuildMixin):
    def dispatch(self, request, *args, **kwargs):
        if not chan_exists(request, *args, **kwargs):
            return redirect("guild:home")

        return super().dispatch(request, *args, **kwargs)
