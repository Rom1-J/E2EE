import uuid

from django.http import Http404

from .models import Guild


def get_guild(guild_id: uuid.UUID) -> Guild:
    guild = Guild.objects.get(id=guild_id)

    if guild:
        return guild

    raise Http404()
