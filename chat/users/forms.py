from allauth.account.adapter import get_adapter
from allauth.account.forms import SignupForm as AllauthSignupForm
from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.handlers.wsgi import WSGIRequest
from django.utils.translation import gettext_lazy as _

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

    def save(self, request: WSGIRequest, *args, **kwargs):
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
