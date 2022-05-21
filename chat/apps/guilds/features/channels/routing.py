from django.urls import re_path

from .consumers import consumers


websocket_urlpatterns = [
    re_path(
        r"^(?P<guild_id>[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12})"
        r"/(?P<channel_id>[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12})$",
        consumers.ChatConsumer.as_asgi(),
    ),
]
