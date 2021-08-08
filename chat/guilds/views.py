import string
import random
import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .features.invites.models import Invite

from .forms import GuildCreationForm
from .mixins import IsInGuildMixin
from .models import Guild
from .utils import get_guild

template_path = "guild/"


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

            return redirect(
                "guild:guild_invites", guild_id=str(form.instance.uuid)
            )

        return render(request, self.template_name, {"form": form})


# =============================================================================
# Guild Routes
# =============================================================================


class GuildDetailView(IsInGuildMixin, View):
    template_name = template_path + "details.html"

    def get(self, request: WSGIRequest, guild_id: uuid.UUID) -> HttpResponse:
        guilds = Guild.objects.filter(members__in=[request.user])
        guild = get_guild(guild_id)

        return render(
            request, self.template_name, {"guild": guild, "guilds": guilds}
        )


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
