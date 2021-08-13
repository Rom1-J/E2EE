from django.urls import path

from .views import (
    GuildChannelCreateView,
    GuildChannelEditView,
    GuildChannelDetailView,
)

urlpatterns = [
    path(
        "<uuid:guild_id>/create/",
        view=GuildChannelCreateView.as_view(),
        name="channel_create",
    ),
    path(
        "<uuid:guild_id>/edit",
        view=GuildChannelEditView.as_view(),
        name="channel_edit",
    ),
    path(
        "<uuid:guild_id>/<uuid:channel_id>/",
        view=GuildChannelDetailView.as_view(),
        name="channel_details",
    ),
]
