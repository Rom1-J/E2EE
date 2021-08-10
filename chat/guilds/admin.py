from django.contrib import admin

from .models import Guild
from .features.invites.models import Invite
from .features.channels.models import Category, Channel, Message


@admin.register(Guild)
class GuildAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "members",
                    "avatar",
                    "categories",
                    "channels",
                )
            },
        ),
    )
    list_display = [
        "id",
        "uuid",
        "name",
        "get_absolute_url",
        "members_count",
        "categories_count",
        "channels_count",
    ]
    search_fields = ["name"]


# =============================================================================


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    fieldsets = ((None, {"fields": ("guild", "key", "uses", "author")}),)
    list_display = ["guild", "key", "uses"]
    search_fields = ["guild", "key"]


# =============================================================================


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = ((None, {"fields": ("name", "channels", "position")}),)
    list_display = ["name", "channels_count"]
    search_fields = ["name"]


# =============================================================================


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    fieldsets = ((None, {"fields": ("name", "position")}),)
    list_display = ["uuid", "name", "messages_count"]
    search_fields = ["name", "uuid"]


# =============================================================================


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    fieldsets = ((None, {"fields": ("author", "content")}),)
    list_display = ["uuid", "author", "content", "created_at", "updated_at"]
    search_fields = ["author", "content", "uuid"]
