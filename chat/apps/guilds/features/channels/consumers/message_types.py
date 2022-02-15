import enum
import json
from typing import NamedTuple


class MessageTypes(enum.EnumMeta):
    def __contains__(cls, item):
        return item in [v.value for v in cls.__members__.values()]


class OutgoingMessageTypes(str, enum.Enum, metaclass=MessageTypes):
    TextMessage = "TEXT_MESSAGE"
    MessageIdCreated = "MESSAGE_ID_CREATED"
    NewUnreadCount = "NEW_UNREAD_COUNT"

    ErrorOccurred = "ERROR_OCCURRED"


class IngoingMessageTypes(str, enum.Enum, metaclass=MessageTypes):
    PostMessage = "POST_MESSAGE"
    ReadMessage = "READ_MESSAGE"
    DeleteMessage = "DELETE_MESSAGE"

    ErrorOccurred = "ERROR_OCCURRED"


class OutgoingEventMessageRead(NamedTuple):
    message_id: int
    sender: str
    receiver: str
    type: str = "message_read"

    def to_json(self) -> str:
        return json.dumps(
            {
                "cmd": IngoingMessageTypes.ReadMessage,
                "message_id": self.message_id,
                "sender": self.sender,
                "receiver": self.receiver,
            }
        )


class OutgoingEventNewMessage(NamedTuple):
    random_id: int
    text: str
    sender: str
    receiver: str
    sender_username: str
    type: str = "new_text_message"

    def to_json(self) -> str:
        return json.dumps(
            {
                "cmd": OutgoingMessageTypes.TextMessage,
                "random_id": self.random_id,
                "text": self.text,
                "sender": self.sender,
                "receiver": self.receiver,
                "sender_username": self.sender_username,
            }
        )


class OutgoingEventNewUnreadCount(NamedTuple):
    sender: str
    unread_count: int
    type: str = "new_unread_count"

    def to_json(self) -> str:
        return json.dumps(
            {
                "cmd": OutgoingMessageTypes.NewUnreadCount,
                "sender": self.sender,
                "unread_count": self.unread_count,
            }
        )


class OutgoingEventMessageIdCreated(NamedTuple):
    random_id: int
    db_id: int
    type: str = "message_id_created"

    def to_json(self) -> str:
        return json.dumps(
            {
                "cmd": OutgoingMessageTypes.MessageIdCreated,
                "random_id": self.random_id,
                "db_id": self.db_id,
            }
        )
