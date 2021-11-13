from django.contrib import admin

from .models import Attachment, Channel, Message


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    fieldsets = ((None, {"fields": ("name", "position", "messages")}),)
    list_display = ["id", "name", "last_message_at", "messages_count"]
    search_fields = ["name", "id"]


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
