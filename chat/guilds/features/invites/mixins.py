from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import Invite


def owns_invitation(request, *args, **kwargs):
    invite_key: str = kwargs.pop("invite_key", "")

    if invite_key:
        query = Q(author=request.user)
        query.add(Q(guild__owner=request.user), Q.OR)
        query.add(Q(key=invite_key), Q.AND)

        return Invite.objects.filter(query).first()

    return False


class OwnsInvitationMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not owns_invitation(request, *args, **kwargs):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
