import uuid
from typing import Optional, Dict, Any

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from ...models import Guild
from ...views import template_path
from ...mixins import IsInGuildMixin

from ...utils import get_guild


class GuildDetailView(IsInGuildMixin, View):
    template_name = template_path + "details.html"

    def get(
        self,
        request: WSGIRequest,
        guild_id: uuid.UUID,
        channel_id: Optional[uuid.UUID] = None,
    ) -> HttpResponse:
        guilds = Guild.objects.filter(members__in=[request.user])
        guild = get_guild(guild_id)

        params: Dict[str, Any] = {"guild": guild, "guilds": guilds}

        if channel_id:
            channel = guild.channels.filter(uuid=channel_id).first()

            if not channel:
                return redirect("guild:guild_view", guild_id=str(guild_id))

            params["channel"] = channel

        return render(request, self.template_name, params)
