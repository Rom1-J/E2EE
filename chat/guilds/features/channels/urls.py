from django.urls import path

from .views import GuildDetailView

urlpatterns = [
    path(
        "<uuid:guild_id>/channel/create/",
        view=GuildDetailView.as_view(),
        name="channel_create",
    ),
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
