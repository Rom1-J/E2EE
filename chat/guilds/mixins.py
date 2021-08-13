from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from .models import Guild


def is_in_guild(request, *args, **kwargs):
    guild_id: str = str(kwargs.pop("guild_id", ""))

    if guild_id:
        return Guild.objects.filter(
            uuid=guild_id, members__in=[request.user]
        ).exists()

    return False


class IsInGuildMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not is_in_guild(request, *args, **kwargs):
            return redirect("guild:home")

        return super().dispatch(request, *args, **kwargs)
