from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View


template_path = "pages/"


class HomeView(View):
    template_name = template_path + "home.html"

    def get(self, request: WSGIRequest) -> HttpResponse:
        return render(request, self.template_name)


class AboutView(View):
    template_name = template_path + "about.html"

    def get(self, request: WSGIRequest) -> HttpResponse:
        return render(request, self.template_name)
