from django.urls import path

from .views import (
    GuildHomeView,
    GuildDetailView,
    GuildCreateView,
    GuildInviteView,
    GuildCreateInviteView,
    GuildDeleteInviteView,
    GuildMembersView,
)

app_name = "guild"
urlpatterns = [
    path("", view=GuildHomeView.as_view(), name="home"),
    path("create/", view=GuildCreateView.as_view(), name="create"),
    path(
        "<uuid:guild_id>/members/",
        view=GuildMembersView.as_view(),
        name="members",
    ),
    path(
        "<uuid:guild_id>/invite/",
        view=GuildInviteView.as_view(),
        name="invite",
    ),
    path(
        "<uuid:guild_id>/invite/<str:key>",
        view=GuildCreateInviteView.as_view(),
        name="invite_join",
    ),
    path(
        "<uuid:guild_id>/invite/<str:key>/delete",
        view=GuildDeleteInviteView.as_view(),
        name="invite_delete",
    ),
    path("<uuid:guild_id>/", view=GuildDetailView.as_view(), name="detail"),
]
