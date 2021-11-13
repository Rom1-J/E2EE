from django.urls import path

from .features.channels.urls import urlpatterns as channels_routes
from .features.invites.urls import urlpatterns as invites_routes
from .views import (
    GuildCreateView,
    GuildDetailView,
    GuildHomeView,
    GuildInvitesView,
    GuildJoinView,
    GuildMembersView,
    GuildSettingsView,
)

app_name = "guild"
urlpatterns = [
    path("", view=GuildHomeView.as_view(), name="home"),
    path("create/", view=GuildCreateView.as_view(), name="create"),
    path("join/", view=GuildJoinView.as_view(), name="join"),
]

# Guild routes
urlpatterns += [
    path(
        "<uuid:guild_id>/",
        view=GuildDetailView.as_view(),
        name="guild_details",
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
    path(
        "<uuid:guild_id>/settings/",
        view=GuildSettingsView.as_view(),
        name="guild_settings",
    ),
]

# Channel routes
urlpatterns += channels_routes

# Invite routes
urlpatterns += invites_routes
