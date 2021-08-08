import uuid
from typing import Dict, Any

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from ...models import Guild
from ...views import template_path
from ...mixins import IsInGuildMixin

from ...utils import get_guild


template_path += "channels/"


def get_params(request: WSGIRequest, guild_id: uuid.UUID) -> Dict[str, Any]:
    guilds = Guild.objects.filter(members__in=[request.user])
    guild = get_guild(guild_id)

    return {"guild": guild, "guilds": guilds}


# =============================================================================


class GuildChannelCreateView(IsInGuildMixin, View):
    template_name = template_path + "create.html"

    def get(
        self,
        request: WSGIRequest,
        guild_id: uuid.UUID,
    ) -> HttpResponse:
        return render(
            request, self.template_name, get_params(request, guild_id)
        )


# =============================================================================


class GuildChannelEditView(IsInGuildMixin, View):
    template_name = template_path + "edit.html"

    def get(
        self,
        request: WSGIRequest,
        guild_id: uuid.UUID,
    ) -> HttpResponse:
        return render(
            request, self.template_name, get_params(request, guild_id)
        )


# =============================================================================


class GuildChannelDetailView(IsInGuildMixin, View):
    template_name = template_path + "details.html"

    def get(
        self,
        request: WSGIRequest,
        guild_id: uuid.UUID,
        channel_id: uuid.UUID,
    ) -> HttpResponse:
        params = get_params(request, guild_id)

        channel = params["guild"].channels.filter(uuid=channel_id).first()

        if not channel:
            return redirect("guild:guild_view", guild_id=str(guild_id))

        params["channel"] = channel

        return render(request, self.template_name, params)
