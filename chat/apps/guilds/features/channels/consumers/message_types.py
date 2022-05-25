import enum
import json
from typing import NamedTuple


class MessageTypes(enum.EnumMeta):
    def __contains__(cls, item):
        return item in [v.value for v in cls.__members__.values()]


class OutgoingMessageTypes(str, enum.Enum, metaclass=MessageTypes):
    TextMessage = "TEXT_MESSAGE"
    MessageIdCreated = "MESSAGE_ID_CREATED"
    GiveMembersPubKeys = "GIVE_MEMBERS_PUB_KEYS"
    NewUnreadCount = "NEW_UNREAD_COUNT"

    ErrorOccurred = "ERROR_OCCURRED"


class IngoingMessageTypes(str, enum.Enum, metaclass=MessageTypes):
    PostMessage = "POST_MESSAGE"
    ReadMessage = "READ_MESSAGE"
    DeleteMessage = "DELETE_MESSAGE"

    ErrorOccurred = "ERROR_OCCURRED"
