import string
import random
import uuid

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views import View

from .forms import GuildCreationForm
from .models import Guild, Invite

template_path = "guild/"


def is_in_guild(request, *args, **kwargs):
    guild_id: str = str(kwargs.pop("guild_id", ""))

    if guild_id:
        return (
            guild := Guild.objects.filter(uuid=guild_id).first()
        ) and request.user in guild.members.all()

    return False


class IsInGuildMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not is_in_guild(request, *args, **kwargs):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


# ============================================================================


class GuildHomeView(LoginRequiredMixin, View):
    template_name = template_path + "home.html"

    def get(self, request: WSGIRequest) -> HttpResponse:
        guilds = Guild.objects.filter(members__in=[request.user])

        return render(request, self.template_name, {"guilds": guilds})


class GuildDetailView(IsInGuildMixin, View):
    template_name = template_path + "detail.html"

    def get(self, request: WSGIRequest, guild_id: uuid.UUID):
        raise Http404()


class GuildInviteView(LoginRequiredMixin, View):
    template_name = template_path + "invite.html"

    def get(self, request: WSGIRequest, guild_id: str, key: str = None):
        if key is None:
            if not is_in_guild(request, guild_id=guild_id):
                return redirect(
                    "guild:create",
                )

            if guild := Guild.objects.filter(id=guild_id).first():
                if not (
                    invite := Invite.objects.filter(guild_id=guild.id).first()
                ):
                    invite = Invite(
                        guild=guild,
                        author=self.request.user,  # type: ignore
                        key="".join(
                            random.choices(string.ascii_letters, k=10)
                        ),
                    )
                    invite.save()

                return render(request, self.template_name, {"invite": invite})

            return redirect("guild:create")

        # pylint: disable=superfluous-parens
        if not (invite := Invite.objects.filter(key=key).first()):
            raise Http404()

        guild = invite.guild

        if request.user in guild.members.all():
            return redirect("guild:detail", guild_id=guild.id)

        invite.uses += 1
        guild.members.add(self.request.user)  # type: ignore
        guild.save()
        invite.save()

        messages.add_message(
            request, messages.INFO, _("Guild joined successfully")
        )

        return redirect("guild:detail", guild_id=guild.id)


class GuildCreateView(LoginRequiredMixin, View):
    template_name = template_path + "create.html"

    def get(self, request: WSGIRequest):
        form = GuildCreationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request: WSGIRequest):
        form = GuildCreationForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            form.instance.members.add(self.request.user)
            form.save()

            return redirect("guild:invite", guild_id=form.instance.pk)

        return render(request, self.template_name, {"form": form})


class GuildDeleteInviteView(IsInGuildMixin, View):
    # noinspection PyMethodMayBeStatic
    def post(self, request: WSGIRequest, guild_id: str, key: str):
        if invite := Invite.objects.filter(key=key).first():
            invite.delete()
            messages.add_message(
                request, messages.INFO, _("Invitation deleted successfully")
            )

        return redirect("guild:detail", guild_id=guild_id)


class GuildMembersView(IsInGuildMixin, View):
    template_name = template_path + "members.html"

    def get(self, request: WSGIRequest, guild_id: str):
        if guild := Guild.objects.filter(id=guild_id).first():
            return render(request, self.template_name, {"guild": guild})

        raise Http404()

    def post(self, request: WSGIRequest, guild_id: int):
        raise Http404()
