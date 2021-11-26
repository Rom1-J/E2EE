from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from chat.users.forms import UserChangeForm, UserCreationForm
from chat.users.models import UserSettings

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {"fields": ("username", "password", "settings")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    list_display = ["id", "username", "is_superuser"]
    search_fields = ["username", "id"]


# =============================================================================


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("theme", "language")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "avatar",
                    "bio",
                )
            },
        ),
        (
            _("Client"),
            {"fields": ("collapsed_categories",)},
        ),
    )

    list_display = ["id", "theme", "language"]
    search_fields = ["theme", "language", "id"]
