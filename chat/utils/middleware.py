import re
from typing import Optional

from django.conf import settings
from django.conf.urls.i18n import is_language_prefix_patterns_used
from django.contrib.auth import get_user_model
from django.core.handlers.asgi import ASGIRequest
from django.http import HttpResponse
from django.middleware.locale import LocaleMiddleware
from django.shortcuts import redirect
from django.urls import resolve
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin

User = get_user_model()


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
        request: ASGIRequest, response: HttpResponse
    ) -> HttpResponse:
        if not settings.DEBUG:
            response.content = strip_spaces_in_template(
                response.content.decode("utf-8")
            ).encode("utf-8")
        return response


# =============================================================================


class CustomLocaleMiddleware(LocaleMiddleware):
    @staticmethod
    def process_request(request: ASGIRequest) -> None:  # type: ignore
        urlconf = getattr(request, "urlconf", settings.ROOT_URLCONF)
        (
            i18n_patterns_used,
            prefixed_default_language,
        ) = is_language_prefix_patterns_used(urlconf)
        language = translation.get_language_from_request(
            request, check_path=i18n_patterns_used  # type: ignore
        )
        language_from_path = translation.get_language_from_path(
            request.path_info
        )

        if (
            not language_from_path
            and i18n_patterns_used
            and not prefixed_default_language
        ):
            language = settings.LANGUAGE_CODE

        if request.user.is_authenticated and hasattr(request.user, "settings"):
            language = getattr(request.user.settings, "language", language)  # type: ignore

        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()  # type: ignore


# =============================================================================


class EnsureMnemonicGeneration(MiddlewareMixin):
    @staticmethod
    def process_request(request: ASGIRequest) -> Optional[HttpResponse]:
        # ensure type of User to be our custom model
        if (
            not isinstance(request.user, User)
            or resolve(request.path_info).url_name == "first_connect"
        ):
            return None

        # noinspection PyUnresolvedReferences
        if request.user.is_authenticated and request.user.first_connect:
            return redirect("users:first_connect")

        return None
