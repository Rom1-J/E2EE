import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from rich.console import Console

console = Console()
User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    room_name: str
    room_group_name: str

    username: str

    # =========================================================================

    @database_sync_to_async
    def get_name(self):
        return User.objects.all()[0].name

    # =========================================================================

    async def connect(self):
        self.room_name = (
            f"{self.scope['url_route']['kwargs']['guild_id']}"
            f"-{self.scope['url_route']['kwargs']['channel_id']}"
        )
        self.room_group_name = "chat_%s" % self.room_name
        self.username = await self.get_name()

        console.log(self.username)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    # =========================================================================

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # =========================================================================

    async def receive(self, text_data: str):
        text_data_json = json.loads(text_data)
        content = text_data_json["content"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "content": content}
        )

    # =========================================================================

    async def chat_message(self, event):
        content = event["content"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"content": content}))

    # =========================================================================
