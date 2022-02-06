from typing import Optional, Tuple

from allauth.account.adapter import get_adapter
from allauth.account.forms import SignupForm as AllauthSignupForm
from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.handlers.asgi import ASGIRequest
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

from ..guilds.features.channels.models import Category
from ..utils.patch_processor import ProcessAction
from .models import UserSettings

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


# =============================================================================


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


# =============================================================================


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings

        fields = ["bio", "avatar", "language", "theme"]

    def clean_field(self):
        data = self.cleaned_data["avatar"]

        if not data:
            data = self.instance.avatar

        return data


# =============================================================================


class SignupForm(AllauthSignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields.pop("email")

    def save(self, request: ASGIRequest, *args, **kwargs):
        adapter = get_adapter(request)
        user = adapter.new_user(request)
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)

        return user


# =============================================================================


class ResetPasswordForm(forms.Form):
    username = forms.CharField(required=True)
    mnemonic = forms.CharField(required=True)

    user: User  # type: ignore

    def clean(self):
        cleaned_data = super().clean()

        if not self.errors:
            self.user = User.objects.filter(
                username=cleaned_data["username"]
            ).first()

            if not (self.user and self.user.mnemonic) or not check_password(
                cleaned_data["mnemonic"], self.user.mnemonic
            ):
                self.add_error("__all__", _("Username or mnemonic incorrect."))


# =============================================================================
# Custom forms
# =============================================================================


def collapse_category(
    request: ASGIRequest, data: dict
) -> Optional[Tuple[bool, dict]]:
    user_settings: UserSettings = request.user.settings  # type: ignore
    category: Category = data["values"]["category"]

    if user_settings.collapsed_categories.filter(id=category.id).exists():
        user_settings.collapsed_categories.remove(category)
    else:
        user_settings.collapsed_categories.add(category)

    return True, {
        "data": {"success": True, "message": "Collapse toggled."},
        "status": 200,
    }


# =============================================================================


def collapse_category_check_category_id(
    request: ASGIRequest, data: dict
) -> Optional[Tuple[bool, dict]]:
    values = data.get("values", {})

    if "category_id" not in values:
        return False, {
            "data": {
                "success": False,
                "message": "Missing field category_id.",
            },
            "status": 400,
        }

    return True, {}


# =============================================================================


def collapse_category_check_existing_category(
    request: ASGIRequest, data: dict
) -> Optional[Tuple[bool, dict]]:
    values = data.get("values", {})

    if not (
        category := Category.objects.filter(
            id=values.get("category_id"), guild__members__in=[request.user]
        ).first()
    ):
        return False, {
            "data": {"success": False, "message": "Category unknown."},
            "status": 400,
        }

    return True, {"category": category}


# =============================================================================


collapse_category_actions = [collapse_category]
collapse_category_checks = [
    collapse_category_check_category_id,
    collapse_category_check_existing_category,
]


class UserClientUpdateProcessAction:
    process = (
        ProcessAction()
        .add_actions("collapse_category", *collapse_category_actions)
        .add_checks("collapse_category", *collapse_category_checks)
    )

    def __init__(self, request: ASGIRequest):
        self.process.process(request)

    def response(self) -> JsonResponse:
        return self.process.response()
