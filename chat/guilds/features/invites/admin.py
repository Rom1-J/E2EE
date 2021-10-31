from django.contrib import admin

from .models import Invite


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    fieldsets = ((None, {"fields": ("guild", "key", "uses", "author")}),)
    list_display = ["guild", "key", "uses"]
    search_fields = ["guild", "key"]
