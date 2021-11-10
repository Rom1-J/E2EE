from django.contrib import admin

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
