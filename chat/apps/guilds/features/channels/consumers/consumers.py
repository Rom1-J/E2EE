import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import escape
from rich import inspect

from chat.apps.guilds.models import Guild
from ..forms import CreateMessageForm
from . import message_types
from ..models import Channel, Message


class ChatConsumer(AsyncWebsocketConsumer):
    room_group_name: str

    # =========================================================================

    @property
    def user(self):
        return self.scope["user"]

    # =========================================================================

    @property
    def guild(self):
        return self.scope["url_route"]["kwargs"]["guild_id"]

    # =========================================================================

    @property
    def channel(self):
        return self.scope["url_route"]["kwargs"]["channel_id"]

    # =========================================================================

    async def connect(self):
        if not self.user.is_authenticated:
            await self.close(code=3000)
            return

        if not await self._can_see(await self._get_channel(self.channel)):
            await self.close(code=3000)
            return

        self.room_group_name = self.guild
        self.room_group_name += "--" + self.channel

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

        await self.give_users()

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
            channel = await self._get_channel(self.channel)
            data |= {"channel": channel, "author": self.user}
            form = CreateMessageForm(data)

            if await database_sync_to_async(form.is_valid)():
                message = await database_sync_to_async(form.save)()
                channel.last_message = message
                await database_sync_to_async(channel.save)()

                response = await self._make_response(message)

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type": "chat.message", "content": json.dumps(response)},
                )

    # =========================================================================

    async def chat_message(self, event):
        await self.send(text_data=event["content"])

    # =========================================================================

    async def give_users(self):
        guild = await self._get_guild(self.guild)

        public_keys = {}

        for member in await self._get_members(guild):
            public_keys[str(member.id)] = member.public_key

        await self.send(text_data=json.dumps({
            "cmd": message_types.OutgoingMessageTypes.GiveMembersPubKeys,
            "data": public_keys
        }))

    # =========================================================================
    # =========================================================================

    @database_sync_to_async
    def _get_channel(self, channel_id: str):
        return Channel.objects.filter(id=channel_id).first()

    # =========================================================================

    @database_sync_to_async
    def _get_guild(self, guild_id: str):
        return Guild.objects.filter(id=guild_id).first()

    # =========================================================================

    @sync_to_async
    def _get_members(self, guild: Guild):
        return list(guild.members.all())

    # =========================================================================

    @database_sync_to_async
    def _can_see(self, channel: Channel):
        return self.user.can_see(channel)

    # =========================================================================

    @database_sync_to_async
    def _make_response(self, message: Message):
        return {
            "cmd": "TEXT_MESSAGE",
            "data": {
                "author": {
                    "id": str(message.author.id),
                    "avatar_url": escape(
                        message.author.settings.avatar.url
                        if message.author.settings.avatar
                        else static("images/icons/circle_user.svg")
                    ),
                    "url": reverse(
                        "users:detail", kwargs={"username": message.author}
                    ),
                    "name": escape(str(message.author)),
                },
                "attachments": [
                    {
                        "file": {
                            "name": escape(f.filename),
                            "url": f.file.url,
                            "size": f.file.size,
                        }
                    }
                    for f in message.attachments.all()
                ],
                "recipient": str(message.recipient.id),
                "content": escape(message.content),
                "nonce": escape(message.nonce),
            }
        }
