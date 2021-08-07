from django.contrib import admin


from .models import Guild, Invite


@admin.register(Guild)
class GroupAdmin(admin.ModelAdmin):
    fieldsets = ((None, {"fields": ("name", "members", "avatar")}),)
    list_display = ["id", "uuid", "name", "members_count", "absolute_url"]
    search_fields = ["name"]


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    fieldsets = ((None, {"fields": ("guild", "key", "uses", "author")}),)
    list_display = ["guild", "key", "uses"]
    search_fields = ["guild", "key"]


# ============================================================================
