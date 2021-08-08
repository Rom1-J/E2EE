from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views import View
from django.utils.translation import gettext as _

from ...views import template_path

from .models import Invite
from .mixins import OwnsInvitationMixin


template_path += "invite/"


class GuildJoinEmptyInviteView(LoginRequiredMixin, View):
    template_name = template_path + "join.html"

    def get(self, request: WSGIRequest) -> HttpResponse:
        return render(request, self.template_name)

    # noinspection PyMethodMayBeStatic
    def post(self, request: WSGIRequest) -> HttpResponse:
        key = request.POST.get("invite_key", "-1").rstrip("/").split("/")[-1]

        return redirect("guild:invite_join", invite_key=key)


# =============================================================================


class GuildJoinInviteView(LoginRequiredMixin, View):
    def get(self, request: WSGIRequest, invite_key: str) -> HttpResponse:
        # pylint: disable=superfluous-parens
        if not (invite := Invite.objects.filter(key=invite_key).first()):
            raise Http404()

        guild = invite.guild

        if request.user in guild.members.all():
            return redirect("guild:guild_details", guild_id=guild.uuid)

        invite.uses += 1
        guild.members.add(self.request.user)  # type: ignore
        guild.save()
        invite.save()

        messages.add_message(
            request, messages.INFO, _("Guild joined successfully")
        )

        return redirect("guild:guild_view", guild_id=guild.uuid)


# =============================================================================


class GuildDeleteInviteView(OwnsInvitationMixin, View):
    # noinspection PyMethodMayBeStatic
    def post(self, request: WSGIRequest, invite_key: str) -> HttpResponse:
        query = Q(author=request.user)
        query.add(Q(guild__owner=request.user), Q.OR)
        query.add(Q(key=invite_key), Q.AND)

        if invite := Invite.objects.filter(query).first():
            guild_id = invite.guild.uuid

            invite.delete()
            messages.add_message(
                request, messages.INFO, _("Invitation deleted successfully")
            )

            return redirect("guild:guild_view", guild_id=guild_id)

        raise Http404()
