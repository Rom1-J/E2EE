from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views import View

from ...views import template_path
from .mixins import OwnsInvitationMixin
from .models import Invite

template_path += "invite/"


class GuildJoinInviteView(LoginRequiredMixin, View):
    def get(self, request: WSGIRequest, invite_key: str) -> HttpResponse:
        # pylint: disable=superfluous-parens
        if not (invite := Invite.objects.filter(key=invite_key).first()):
            raise Http404()

        guild = invite.guild

        if request.user in guild.members.all():
            return redirect("guild:guild_details", guild_id=guild.id)

        invite.uses += 1
        guild.members.add(self.request.user)  # type: ignore
        guild.save()
        invite.save()

        messages.add_message(
            request, messages.INFO, _("Guild joined successfully")
        )

        return redirect("guild:guild_details", guild_id=guild.id)


# =============================================================================


class GuildDeleteInviteView(OwnsInvitationMixin, View):
    # noinspection PyMethodMayBeStatic
    def post(self, request: WSGIRequest, invite_key: str) -> HttpResponse:
        query = Q(author=request.user)
        query.add(Q(guild__owner=request.user), Q.OR)
        query.add(Q(key=invite_key), Q.AND)

        if invite := Invite.objects.filter(query).first():
            guild_id = invite.guild.id

            invite.delete()
            messages.add_message(
                request, messages.SUCCESS, _("Invitation deleted successfully")
            )

            return redirect("guild:guild_details", guild_id=guild_id)

        raise Http404()
