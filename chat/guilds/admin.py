from django.contrib import admin

from .features.channels.models import Attachment, Category, Channel, Message
from .features.invites.models import Invite
from .models import Guild


@admin.register(Guild)
class GuildAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "description",
                    "avatar",
                    "owner",
                    "members",
                    "channels",
                    "categories",
                )
            },
        ),
    )
    list_display = [
        "id",
        "name",
        "get_absolute_url",
        "members_count",
    ]
    search_fields = ["name"]


# =============================================================================
# Features admin
# =============================================================================


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    fieldsets = ((None, {"fields": ("guild", "key", "uses", "author")}),)
    list_display = ["guild", "key", "uses"]
    search_fields = ["guild", "key"]


# =============================================================================
# =============================================================================


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = ((None, {"fields": ("name", "position", "guild")}),)
    list_display = ["id", "name", "guild", "position", "channels_count"]
    search_fields = ["id", "name"]


# =============================================================================


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("name", "topic", "position", "parent", "guild")}),
    )
    list_display = [
        "id",
        "name",
        "guild",
        "position",
        "parent",
        "last_message",
        "messages_count",
    ]
    search_fields = ["id", "name"]


# =============================================================================


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("author", "channel", "content", "attachments")}),
    )
    list_display = [
        "id",
        "author",
        "content",
        "channel",
        "created_at",
        "updated_at",
    ]
    search_fields = ["author", "content", "id"]


# =============================================================================


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    fieldsets = ((None, {"fields": ("file",)}),)
    list_display = ["id", "extension"]
    search_fields = ["id"]
