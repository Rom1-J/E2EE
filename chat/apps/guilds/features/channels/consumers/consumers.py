import json

from channels.generic.websocket import AsyncWebsocketConsumer
from rich import inspect

from ..forms import CreateMessageForm
from . import message_types


class ChatConsumer(AsyncWebsocketConsumer):
    room_name: str
    room_group_name: str

    # =========================================================================

    @property
    def user(self):
        return self.scope["user"]

    # =========================================================================

    async def connect(self):
        if not self.user.is_authenticated:
            await self.close(code=3000)
            return

        self.room_name = str(self.user.pk)

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    # =========================================================================

    async def disconnect(self, close_code):
        if close_code != 1001 and hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

    # =========================================================================

    async def receive(self, text_data: str):
        try:
            text_data_json = json.loads(text_data)
            if not (cmd := text_data_json.get("cmd")):
                payload = {
                    "error": True,
                    "cmd": message_types.IngoingMessageTypes.ErrorOccurred,
                    "message": "Missing cmd",
                }

                await self.send(text_data=json.dumps(payload))
                return

            if not (data := text_data_json.get("data")):
                payload = {
                    "error": True,
                    "cmd": message_types.IngoingMessageTypes.ErrorOccurred,
                    "message": "Missing data",
                }

                await self.send(text_data=json.dumps(payload))
                return

            if cmd not in message_types.IngoingMessageTypes:
                payload = {
                    "error": True,
                    "cmd": message_types.IngoingMessageTypes.ErrorOccurred,
                    "message": "Unknown cmd passed",
                }

                await self.send(text_data=json.dumps(payload))
                return

            await self.handle_received_message(
                message_types.IngoingMessageTypes(cmd), data
            )

        except json.JSONDecodeError:
            payload = {
                "error": True,
                "cmd": message_types.OutgoingMessageTypes.ErrorOccurred,
                "message": "Improper payload passed",
            }

            await self.send(text_data=json.dumps(payload))

    # =========================================================================
    # =========================================================================

    async def handle_received_message(
        self, cmd: message_types.IngoingMessageTypes, data: dict
    ):
        if cmd == message_types.IngoingMessageTypes.PostMessage:
            form = CreateMessageForm(data)
            inspect(form)

    # =========================================================================

    async def chat_message(self, event):
        content = event["content"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"content": content}))

    # =========================================================================
