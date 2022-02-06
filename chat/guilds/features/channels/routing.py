from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(
        "ws/chat/<uuid:guild_id>/<uuid:channel_id>/",
        consumers.ChatConsumer.as_asgi(),
    ),
]
