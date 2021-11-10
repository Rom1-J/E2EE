from django.shortcuts import redirect

from .models import Guild


def is_in_guild(request, *args, **kwargs):
    guild_id: str = str(kwargs.pop("guild_id", ""))

    if guild_id:
        return Guild.objects.filter(
            id=guild_id, members__in=[request.user]
        ).exists()

    return False


def is_guild_owner(request, *args, **kwargs):
    guild_id: str = str(kwargs.pop("guild_id", ""))

    if guild_id:
        return Guild.objects.filter(
            id=guild_id, owner_id=request.user.id
        ).exists()

    return False


# =============================================================================


class IsInGuildMixin:
    def dispatch(self, request, *args, **kwargs):
        if not is_in_guild(request, *args, **kwargs):
            return redirect("guild:home")

        return super().dispatch(request, *args, **kwargs)  # type: ignore


class IsGuildOwnerMixin(IsInGuildMixin):
    def dispatch(self, request, *args, **kwargs):
        if not is_guild_owner(request, *args, **kwargs):
            return redirect("guild:home")

        return super().dispatch(request, *args, **kwargs)
