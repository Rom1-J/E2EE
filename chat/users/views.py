from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import DetailView, RedirectView, UpdateView
from faker import Faker

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


class UserUpdateView(BaseUsersView, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["username", "avatar", "language", "bio"]
    success_message = _("Information successfully updated")

    def get_object(self):
        return self.request.user


# =============================================================================


class UserRedirectView(BaseUsersView, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse(
            "users:detail", kwargs={"username": self.request.user.username}
        )


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

            return render(
                request,
                self.template_name + "/next.html",
                {"mnemonics": mnemonics},
            )

        return redirect("users:first_connect")
