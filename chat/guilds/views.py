import string
import random
import uuid
from typing import Optional, Any, Dict

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views import View

from .forms import GuildCreationForm
from .mixins import IsInGuildMixin, OwnsInvitationMixin
from .models import Guild, Invite

template_path = "guild/"


def get_guild(guild_id: uuid.UUID) -> Guild:
    guild = Guild.objects.filter(uuid=guild_id).first()

    if guild:
        return guild

    raise Http404()


# =============================================================================


class GuildHomeView(LoginRequiredMixin, View):
    template_name = template_path + "home.html"

    def get(self, request: WSGIRequest) -> HttpResponse:
        guilds = Guild.objects.filter(members__in=[request.user])

        return render(request, self.template_name, {"guilds": guilds})


# =============================================================================


class GuildCreateView(LoginRequiredMixin, View):
    template_name = template_path + "create.html"

    def get(self, request: WSGIRequest) -> HttpResponse:
        form = GuildCreationForm(user=request.user)

        return render(request, self.template_name, {"form": form})

    def post(self, request: WSGIRequest) -> HttpResponse:
        form = GuildCreationForm(
            request.POST, request.FILES, user=request.user
        )

        if form.is_valid():
            form.save()
            form.instance.members.add(self.request.user)
            form.save()

            return redirect("guild:invites", guild_id=str(form.instance.uuid))

        return render(request, self.template_name, {"form": form})


# =============================================================================
# Guild Routes
# =============================================================================


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
                return redirect("guild:view", guild_id=str(guild_id))

            params["channel"] = channel

        return render(request, self.template_name, params)


# =============================================================================


class GuildInvitesView(IsInGuildMixin, View):
    template_name = template_path + "invite.html"

    def get(self, request: WSGIRequest, guild_id: uuid.UUID) -> HttpResponse:
        guild = get_guild(guild_id)

        if not (invite := Invite.objects.filter(guild_id=guild.id).first()):
            invite = Invite(
                guild=guild,
                author=self.request.user,  # type: ignore
                key="".join(random.choices(string.ascii_letters, k=10)),
            )
            invite.save()

        return render(request, self.template_name, {"invite": invite})


# =============================================================================


class GuildMembersView(IsInGuildMixin, View):
    template_name = template_path + "members.html"

    def get(self, request: WSGIRequest, guild_id: uuid.UUID) -> HttpResponse:
        guild = get_guild(guild_id)

        return render(request, self.template_name, {"guild": guild})

    def post(self, request: WSGIRequest, guild_id: int) -> HttpResponse:
        raise Http404()


# =============================================================================
# Invite Routes
# =============================================================================


class GuildJoinEmptyInviteView(LoginRequiredMixin, View):
    template_name = template_path + "join_invite.html"

    def get(self, request: WSGIRequest) -> HttpResponse:
        return render(request, self.template_name)

    # noinspection PyMethodMayBeStatic
    def post(self, request: WSGIRequest) -> HttpResponse:
        key = request.POST.get("invite_key", "-1").split("/")[-1]

        return redirect("guild:invite_join", key=key)


# =============================================================================


class GuildJoinInviteView(LoginRequiredMixin, View):
    def get(self, request: WSGIRequest, invite_key: str) -> HttpResponse:
        # pylint: disable=superfluous-parens
        if not (invite := Invite.objects.filter(key=invite_key).first()):
            raise Http404()

        guild = invite.guild

        if request.user in guild.members.all():
            return redirect("guild:detail", guild_id=guild.uuid)

        invite.uses += 1
        guild.members.add(self.request.user)  # type: ignore
        guild.save()
        invite.save()

        messages.add_message(
            request, messages.INFO, _("Guild joined successfully")
        )

        return redirect("guild:detail", guild_id=guild.uuid)


# =============================================================================


class GuildDeleteInviteView(OwnsInvitationMixin, View):
    # noinspection PyMethodMayBeStatic
    def post(self, request: WSGIRequest, invite_key: str) -> HttpResponse:
        if invite := Invite.objects.filter(
            key=invite_key, author=request.user  # type: ignore
        ).first():
            guild_id = invite.guild.uuid

            invite.delete()
            messages.add_message(
                request, messages.INFO, _("Invitation deleted successfully")
            )

            return redirect("guild:view", guild_id=guild_id)

        raise Http404()
