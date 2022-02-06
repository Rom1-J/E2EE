from django.core.handlers.asgi import ASGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import View

template_path = "pages/"


class HomeView(View):
    # noinspection PyMethodMayBeStatic
    def get(self, request: ASGIRequest) -> HttpResponse:
        return redirect("guild:home")
