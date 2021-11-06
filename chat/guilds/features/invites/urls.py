from django.urls import path

from .views import (
    GuildJoinInviteView,
    GuildDeleteInviteView,
)

urlpatterns = [
    path(
        "invite/<str:invite_key>/",
        view=GuildJoinInviteView.as_view(),
        name="invite_join",
    ),
    path(
        "invite/<str:invite_key>/delete/",
        view=GuildDeleteInviteView.as_view(),
        name="invite_delete",
    ),
]
