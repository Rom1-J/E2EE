from django.urls import path

from .features.channels.urls import urlpatterns as channels_routes
from .features.invites.urls import urlpatterns as invites_routes
from .views import (
    GuildCreateView,
    GuildDetailView,
    GuildHomeView,
    GuildInvitesView,
    GuildJoinView,
    GuildSettingsChannelsView,
    GuildSettingsHomeView,
    GuildSettingsMembersView,
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
        "<uuid:guild_id>/invites/",
        view=GuildInvitesView.as_view(),
        name="guild_invites",
    ),
    path(
        "<uuid:guild_id>/settings/",
        view=GuildSettingsHomeView.as_view(),
        name="guild_settings",
    ),
    path(
        "<uuid:guild_id>/settings/members/",
        view=GuildSettingsMembersView.as_view(),
        name="guild_settings_members",
    ),
    path(
        "<uuid:guild_id>/settings/channels/",
        view=GuildSettingsChannelsView.as_view(),
        name="guild_settings_channels",
    ),
]

# Channel routes
urlpatterns += channels_routes

# Invite routes
urlpatterns += invites_routes
