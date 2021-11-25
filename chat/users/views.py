from allauth.account.utils import user_pk_to_url_str
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import DetailView, RedirectView
from faker import Faker

from .forms import ResetPasswordForm, UserSettingsForm

User = get_user_model()
template_path = "users/"

locales = {}
for lang_key, lang_name in settings.LANGUAGES:
    locales[lang_key] = lang_name

fake = Faker(list(locales.keys()))


class BaseUsersView(LoginRequiredMixin):
    pass


# =============================================================================


class UserDetailView(BaseUsersView, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


# =============================================================================


class UserRedirectView(BaseUsersView, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse(
            "users:detail", kwargs={"username": self.request.user.username}
        )


# =============================================================================


class UserUpdateView(BaseUsersView, View):
    template_name = template_path + "settings.html"

    def get(self, request: WSGIRequest) -> HttpResponse:
        form = UserSettingsForm(instance=request.user.settings)  # type: ignore

        return render(request, self.template_name, {"form": form})

    def post(self, request: WSGIRequest) -> HttpResponse:
        form = UserSettingsForm(request.POST, instance=request.user.settings)  # type: ignore

        if form.is_valid():
            form.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                _("Information updated successfully"),
            )

            return redirect("users:redirect")

        return render(request, self.template_name, {"form": form})


# =============================================================================


class UserResetPasswordView(View):
    template_name = template_path + "reset_password.html"

    def get(self, request: WSGIRequest) -> HttpResponse:
        form = ResetPasswordForm()

        return render(request, self.template_name, {"form": form})

    def post(self, request: WSGIRequest) -> HttpResponse:
        form = ResetPasswordForm(request.POST)

        if form.is_valid():
            return redirect(
                "account_reset_password_from_key",
                uidb36=user_pk_to_url_str(form.user),
                key=default_token_generator.make_token(form.user),
            )

        return render(request, self.template_name, {"form": form})


# =============================================================================


class UserFistConnectView(BaseUsersView, View):
    template_name = template_path + "first_connect"

    def get(self, request: WSGIRequest, page: str = "first") -> HttpResponse:
        if page == "first":
            return render(request, self.template_name + "/first.html")

        if page == "next":
            mnemonics = {
                locale: " ".join(fake[k].words(nb=10))  # type: ignore
                for k, locale in locales.items()
            }

            request.session["mnemonics"] = mnemonics

            return render(
                request,
                self.template_name + "/next.html",
                {"mnemonics": mnemonics},
            )

        return redirect("users:first_connect")

    def post(self, request: WSGIRequest, page: str = "first") -> HttpResponse:
        if page != "next":
            return redirect("users:first_connect")

        mnemonic = request.POST.get("mnemonic")
        mnemonics = request.session["mnemonics"]

        if mnemonic not in mnemonics.values():
            messages.add_message(
                request,
                messages.WARNING,
                _("Please do not edit proposed mnemonics"),
            )
            return render(
                request,
                self.template_name + "/next.html",
                {"mnemonics": mnemonics},
            )

        del request.session["mnemonics"]

        user = User.objects.get(id=request.user.id)
        user.mnemonic = make_password(mnemonic)
        user.first_connect = False
        user.save()

        messages.add_message(
            request,
            messages.INFO,
            f'"{mnemonic}" '
            + _(
                "has been set as your mnemonic, remember not to lose it under any circumstances!"
            ),
        )

        return redirect("users:detail", username=request.user.username)
