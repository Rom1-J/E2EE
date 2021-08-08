from django.urls import path

from .views import (
    GuildHomeView,
    GuildCreateView,
    GuildDetailView,
    GuildInvitesView,
    GuildMembersView,
    GuildJoinEmptyInviteView,
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
    path(
        "<uuid:guild_id>/", view=GuildDetailView.as_view(), name="guild_view"
    ),
    path(
        "<uuid:guild_id>/members/",
        view=GuildMembersView.as_view(),
        name="guild_members",
    ),
    path(
        "<uuid:guild_id>/invites/",
        view=GuildInvitesView.as_view(),
        name="guild_invites",
    ),
]

# Channel routes
urlpatterns += [
    path(
        "<uuid:guild_id>/channel/<uuid:channel_id>/",
        view=GuildDetailView.as_view(),
        name="channel_details",
    ),
    path(
        "<uuid:guild_id>/channel/<uuid:channel_id>/",
        view=GuildDetailView.as_view(),
        name="channel_edit",
    ),
]

# Invite routes
urlpatterns += [
    path(
        "invite/",
        view=GuildJoinEmptyInviteView.as_view(),
        name="invite_empty_join",
    ),
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
