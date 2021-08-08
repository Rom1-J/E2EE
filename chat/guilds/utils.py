import uuid

from django.http import Http404

from .models import Guild


def get_guild(guild_id: uuid.UUID) -> Guild:
    guild = Guild.objects.filter(uuid=guild_id).first()

    if guild:
        return guild

    raise Http404()
