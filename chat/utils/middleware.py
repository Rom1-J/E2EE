import re
from typing import Optional

from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import resolve
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from rich import inspect

from chat.users.models import User


def strip_spaces_in_template(template_source):
    """
    Default function used to preprocess templates.
    To use Your own stripping function do not change this function, use
    **settings.TEMPLATE_MINIFIER_STRIP_FUNCTION property**!

    https://github.com/martinsvoboda/django-template-minifying-loader/blob/master/template_minifying_loader/utils.py
    """

    # remove comments
    template_source = re.sub(r"{#.*#}", "", template_source)

    # strip whitespace between html tags
    template_source = re.sub(
        r">\s+<", "><", template_source, flags=re.MULTILINE
    )

    # strip whitespace around django variables
    template_source = re.sub(
        r">\s+{{", ">{{", template_source, flags=re.MULTILINE
    )
    template_source = re.sub(
        r"}}\s+<", "}}<", template_source, flags=re.MULTILINE
    )

    # strip whitespace around django and html tags
    template_source = re.sub(
        r">\s+{%", ">{%", template_source, flags=re.MULTILINE
    )
    template_source = re.sub(
        r"%}\s+<", "%}<", template_source, flags=re.MULTILINE
    )

    # strip whitespace between django tags
    template_source = re.sub(
        r"%}\s+{%", "%}{%", template_source, flags=re.MULTILINE
    )

    # strip whitespace between django tags and variables
    template_source = re.sub(
        r"%}\s+{{", "%}{{", template_source, flags=re.MULTILINE
    )
    template_source = re.sub(
        r"}}\s+{%", "}}{%", template_source, flags=re.MULTILINE
    )

    # condense any white space
    template_source = re.sub(
        r"\s{2,}", " ", template_source, flags=re.MULTILINE
    )

    # strip leading and trailing html
    template_source = template_source.strip()

    return template_source


class SpacelessMiddleware(MiddlewareMixin):
    @staticmethod
    def process_response(
        request: WSGIRequest, response: HttpResponse
    ) -> HttpResponse:
        if not settings.DEBUG:
            response.content = strip_spaces_in_template(
                response.content.decode("utf-8")
            ).encode("utf-8")
        return response


# =============================================================================


class ForceDefaultLanguageMiddleware(MiddlewareMixin):
    @staticmethod
    def process_response(
        request: WSGIRequest, response: HttpResponse
    ) -> HttpResponse:
        response.LANG = getattr(  # type: ignore
            request.user, "language", settings.LANGUAGE_CODE
        )

        translation.activate(response.LANG)  # type: ignore
        response.LANGUAGE_CODE = response.LANG  # type: ignore

        return response


# =============================================================================


class EnsureMnemonicGeneration(MiddlewareMixin):
    @staticmethod
    def process_request(request: WSGIRequest) -> Optional[HttpResponse]:
        # ensure type of User to be our custom model
        if (
            not isinstance(request.user, User)
            or resolve(request.path_info).url_name == "first_connect"
        ):
            return None

        if request.user.is_authenticated and request.user.first_connect:
            return redirect("users:first_connect")

        return None
