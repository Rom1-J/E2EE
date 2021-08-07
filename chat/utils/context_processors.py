from django.conf import settings


def settings_context(request):
    return {
        "DEBUG": settings.DEBUG,
        "APP_NAME": settings.APP_NAME,

        "SHOW_SIDEBAR": request.resolver_match.url_name in ["about"]
    }
