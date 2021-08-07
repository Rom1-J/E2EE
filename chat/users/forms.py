from allauth.account.forms import LoginForm as AllauthLoginForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.forms.utils import ErrorList
from django.utils.html import format_html, format_html_join
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


# =============================================================================


class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ""

        return format_html(
            "<div>{}</div>",
            format_html_join("", "<div>{}</div>", ((e,) for e in self)),
        )


class LoginForm(AllauthLoginForm):
    def __init__(self, *args, **kwargs):
        kwargs["error_class"] = DivErrorList

        super(LoginForm, self).__init__(*args, **kwargs)
