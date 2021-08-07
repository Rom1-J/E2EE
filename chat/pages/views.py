from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import View


template_path = "pages/"


class HomeView(View):
    # noinspection PyMethodMayBeStatic
    def get(self, request: WSGIRequest) -> HttpResponse:
        return redirect("guild:home")
