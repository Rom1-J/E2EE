from django.contrib import admin

from .models import Channel, Message, Attachment


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    fieldsets = ((None, {"fields": ("name", "position", "messages")}),)
    list_display = ["uuid", "name", "last_message_at", "messages_count"]
    search_fields = ["name", "uuid"]


# =============================================================================


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("author", "channel", "content", "attachments")}),
    )
    list_display = [
        "uuid",
        "author",
        "content",
        "channel",
        "created_at",
        "updated_at",
    ]
    search_fields = ["author", "content", "uuid"]


# =============================================================================


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    fieldsets = ((None, {"fields": ("file",)}),)
    list_display = ["uuid", "extension"]
    search_fields = ["uuid"]
