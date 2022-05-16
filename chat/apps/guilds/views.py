import uuid

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.asgi import ASGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _
from django.views import View
from rich import inspect

from .features.channels.models import Channel
from .features.invites.models import Invite
from .forms import (
    GuildChangeForm,
    GuildCategoriesForm,
    GuildChannelsForm,
    GuildCreationForm,
    GuildMembersForm,
    GuildSettingsChannelsProcessAction,
)
from .mixins import IsGuildOwnerMixin, IsInGuildMixin
from .models import Guild
from .utils import get_guild

template_path = "guild/"
User = get_user_model()


# =============================================================================


class GuildHomeView(LoginRequiredMixin, View):
    template_name = template_path + "home.html"

    def get(self, request: ASGIRequest) -> HttpResponse:
        guilds = Guild.objects.filter(members__in=[request.user])

        return render(request, self.template_name, {"guilds": guilds})


# =============================================================================


class GuildCreateView(LoginRequiredMixin, View):
    template_name = template_path + "create.html"

    def get(self, request: ASGIRequest) -> HttpResponse:
        form = GuildCreationForm(user=request.user)

        return render(request, self.template_name, {"form": form})

    def post(self, request: ASGIRequest) -> HttpResponse:
        form = GuildCreationForm(
            request.POST, request.FILES, user=request.user
        )

        if form.is_valid():
            form.save()
            form.instance.members.add(self.request.user)
            form.save()

            return redirect(
                "guild:guild_invites", guild_id=str(form.instance.id)
            )

        return render(request, self.template_name, {"form": form})


# =============================================================================


class GuildJoinView(LoginRequiredMixin, View):
    template_name = template_path + "join.html"

    def get(self, request: ASGIRequest) -> HttpResponse:
        return render(request, self.template_name)

    # noinspection PyMethodMayBeStatic
    def post(self, request: ASGIRequest) -> HttpResponse:
        key = request.POST.get("invite_key", "-1").rstrip("/").split("/")[-1]

        return redirect("guild:invite_join", invite_key=key)


# =============================================================================
# Guild Routes
# =============================================================================


class GuildOwnerView(LoginRequiredMixin, IsGuildOwnerMixin, View):
    def dispatch(
        self, request, *args, **kwargs
    ):  # pylint: disable=useless-super-delegation
        return super().dispatch(request, *args, **kwargs)


class BaseGuildView(LoginRequiredMixin, IsInGuildMixin, View):
    def dispatch(
        self, request, *args, **kwargs
    ):  # pylint: disable=useless-super-delegation
        return super().dispatch(request, *args, **kwargs)


class BaseGuildSettingsView(GuildOwnerView):
    template_path = template_path + "settings/"

    def dispatch(
        self, request, *args, **kwargs
    ):  # pylint: disable=useless-super-delegation
        return super().dispatch(request, *args, **kwargs)


# =============================================================================


class GuildDetailView(BaseGuildView):
    template_name = template_path + "details.html"

    def get(self, request: ASGIRequest, guild_id: uuid.UUID) -> HttpResponse:
        guilds = Guild.objects.filter(members__in=[request.user])
        guild = get_guild(guild_id)

        latest_channels = Channel.objects.filter(guild=guild).all()

        return render(
            request,
            self.template_name,
            {
                "guild": guild,
                "guilds": guilds,
                "latest_channels": latest_channels,
            },
        )


# =============================================================================


class GuildInvitesView(BaseGuildView):
    template_name = template_path + "invite.html"

    def get(self, request: ASGIRequest, guild_id: uuid.UUID) -> HttpResponse:
        guild = get_guild(guild_id)

        if not (invite := Invite.objects.filter(guild_id=guild.id).first()):
            invite = Invite(
                guild=guild,
                author=self.request.user,  # type: ignore
            )
            invite.save()

        return render(request, self.template_name, {"invite": invite})


# =============================================================================


class GuildSettingsHomeView(BaseGuildSettingsView):
    template_name = BaseGuildSettingsView.template_path + "settings.html"

    def get(self, request: ASGIRequest, guild_id: uuid.UUID) -> HttpResponse:
        guild = get_guild(guild_id)
        form = GuildChangeForm(instance=guild)

        return render(
            request, self.template_name, {"form": form, "guild": guild}
        )

    def post(self, request: ASGIRequest, guild_id: uuid.UUID) -> HttpResponse:
        guild = get_guild(guild_id)
        form = GuildChangeForm(request.POST, request.FILES, instance=guild)

        if form.is_valid():
            form.save()

            return redirect(
                "guild:guild_details", guild_id=str(form.instance.id)
            )

        return render(
            request, self.template_name, {"form": form, "guild": guild}
        )


# =============================================================================


class GuildSettingsMembersView(BaseGuildSettingsView):
    template_name = BaseGuildSettingsView.template_path + "members.html"

    def get(self, request: ASGIRequest, guild_id: uuid.UUID) -> HttpResponse:
        guild = get_guild(guild_id)
        form = GuildMembersForm(instance=guild)

        return render(
            request, self.template_name, {"form": form, "guild": guild}
        )

    def post(self, request: ASGIRequest, guild_id: uuid.UUID) -> HttpResponse:
        guild = get_guild(guild_id)
        form = GuildMembersForm(request.POST, instance=guild)

        if form.is_valid() and (members := form.data.get("members")):
            if form.data.get("action") == "kick":
                for member in members:
                    guild.members.remove(User.objects.get(id=member))

                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f"{len(members)} {_('members kicked')}",
                )

            elif form.data.get("action") == "ban":
                messages.add_message(
                    request, messages.INFO, "Not Implemented Yet"
                )

            return redirect(
                "guild:guild_details", guild_id=str(form.instance.id)
            )

        return render(
            request, self.template_name, {"form": form, "guild": guild}
        )


# =============================================================================


class GuildSettingsChannelsView(BaseGuildSettingsView):
    template_name = BaseGuildSettingsView.template_path + "channels.html"

    def get(self, request: ASGIRequest, guild_id: uuid.UUID) -> HttpResponse:
        guild = get_guild(guild_id)

        categories_form = GuildCategoriesForm(instance=guild)
        channels_form = GuildChannelsForm(instance=guild)

        return render(
            request,
            self.template_name,
            {
                "categories_form": categories_form,
                "channels_form": channels_form,
                "guild": guild,
            },
        )

    def post(self, request: ASGIRequest, guild_id: uuid.UUID) -> HttpResponse:
        guild = get_guild(guild_id)
        categories_form = GuildCategoriesForm(request.POST, guild=guild)
        channels_form = GuildChannelsForm(request.POST, guild=guild)

        if (
            categories_form.is_valid()
            and request.POST.get("type") == "category"
        ):
            categories_form.save()

            return redirect(
                "guild:guild_settings_channels", guild_id=str(guild.id)
            )

        if channels_form.is_valid() and request.POST.get("type") == "channel":
            channels_form.save()

            return redirect(
                "guild:guild_settings_channels", guild_id=str(guild.id)
            )

        return render(
            request,
            self.template_name,
            {
                "categories_form": categories_form,
                "channels_form": channels_form,
                "guild": guild,
            },
        )

    # noinspection PyMethodMayBeStatic
    def patch(self, request: ASGIRequest, guild_id: uuid.UUID) -> JsonResponse:
        guild = get_guild(guild_id)
        return GuildSettingsChannelsProcessAction(request, guild).response()


# =============================================================================
