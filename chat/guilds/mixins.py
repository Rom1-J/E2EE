from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Guild, Invite


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


# =============================================================================


def owns_invitation(request, *args, **kwargs):
    invite_key: str = kwargs.pop("invite_key", "")

    if invite_key:
        return Invite.objects.filter(
            key=invite_key, author=request.user
        ).first()

    return False


class OwnsInvitationMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not owns_invitation(request, *args, **kwargs):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
