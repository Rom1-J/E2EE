import uuid
from typing import Any, Dict

from django.core.handlers.asgi import ASGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from .models import Channel
from ...models import Guild
from ...utils import get_guild
from ...views import BaseGuildView, template_path
from .mixins import ChanExistsMixin

template_path += "channels/"


def get_params(request: ASGIRequest, guild_id: uuid.UUID) -> Dict[str, Any]:
    guilds = Guild.objects.filter(members__in=[request.user])
    guild = get_guild(guild_id)

    return {"guild": guild, "guilds": guilds}


class BaseChannelView(BaseGuildView, ChanExistsMixin):
    pass


# =============================================================================


class GuildChannelCreateView(BaseChannelView):
    template_name = template_path + "create.html"

    def get(
        self,
        request: ASGIRequest,
        guild_id: uuid.UUID,
    ) -> HttpResponse:
        return render(
            request, self.template_name, get_params(request, guild_id)
        )


# =============================================================================


class GuildChannelEditView(BaseChannelView):
    template_name = template_path + "edit.html"

    def get(
        self,
        request: ASGIRequest,
        guild_id: uuid.UUID,
    ) -> HttpResponse:
        return render(
            request, self.template_name, get_params(request, guild_id)
        )


# =============================================================================


class GuildChannelDetailView(BaseChannelView):
    template_name = template_path + "details.html"

    def get(
        self,
        request: ASGIRequest,
        guild_id: uuid.UUID,
        channel_id: uuid.UUID,
    ) -> HttpResponse:
        params = get_params(request, guild_id)
        guild: Guild = params["guild"]

        channel: Channel = guild.channels.get(id__exact=channel_id)

        if not channel:
            return redirect("guild:guild_details", guild_id=str(guild_id))

        params["room_name"] = channel
        params["room_messages"] = channel.get_messages(request.user)

        return render(request, self.template_name, params)

    # =========================================================================

    def post(
        self,
        request: ASGIRequest,
        guild_id: uuid.UUID,
        channel_id: uuid.UUID,
    ) -> JsonResponse:
        result = {}

        return JsonResponse(result)
