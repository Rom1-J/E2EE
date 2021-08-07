from django.urls import path

from .views import (
    GuildHomeView,
    GuildCreateView,
    GuildDetailView,
    GuildInvitesView,
    GuildMembersView,
    GuildJoinInviteView,
    GuildDeleteInviteView,
)

app_name = "guild"
urlpatterns = [
    path("", view=GuildHomeView.as_view(), name="home"),
    path("create/", view=GuildCreateView.as_view(), name="create"),
]

# Guild routes
urlpatterns += [
    path("<uuid:guild_id>/", view=GuildDetailView.as_view(), name="detail"),
    path(
        "<uuid:guild_id>/members/",
        view=GuildMembersView.as_view(),
        name="members",
    ),
    path(
        "<uuid:guild_id>/invites/",
        view=GuildInvitesView.as_view(),
        name="invites",
    ),
]

# Invite routes
urlpatterns += [
    path(
        "invite/<str:key>",
        view=GuildJoinInviteView.as_view(),
        name="invite_join",
    ),
    path(
        "invite/<str:key>/delete",
        view=GuildDeleteInviteView.as_view(),
        name="invite_delete",
    ),
]
