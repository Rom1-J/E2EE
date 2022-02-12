from django.urls import path

from .consumers import consumers

websocket_urlpatterns = [
    path("", consumers.ChatConsumer.as_asgi()),
]
