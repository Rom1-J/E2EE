import re

from django.conf import settings
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin


# https://github.com/martinsvoboda/django-template-minifying-loader/blob/master/template_minifying_loader/utils.py
def strip_spaces_in_template(template_source):
    """
    Default function used to preprocess templates.
    To use Your own stripping function do not change this function, use
    **settings.TEMPLATE_MINIFIER_STRIP_FUNCTION property**!
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
    """trim spaces between tags if not in DEBUG"""

    # pylint: disable=no-self-use
    def process_response(self, request, response):
        if not settings.DEBUG:
            response.content = strip_spaces_in_template(
                response.content.decode("utf-8")
            ).encode("utf-8")
        return response


# =============================================================================


class ForceDefaultLanguageMiddleware(MiddlewareMixin):
    # pylint: disable=no-self-use
    def process_request(self, request):
        if "django_language" not in request.COOKIES.keys():
            request.LANG = getattr(
                settings, "LANGUAGE_CODE", settings.LANGUAGE_CODE
            )
            translation.activate(request.LANG)
            request.LANGUAGE_CODE = request.LANG
