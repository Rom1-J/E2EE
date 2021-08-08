from django.conf import settings


def show_sidebar(url_name: str) -> bool:
    routes = ["guild_view", "channel_"]

    return any(route in url_name for route in routes)


def settings_context(request):
    print(request.resolver_match.url_name)
    return {
        "DEBUG": settings.DEBUG,
        "APP_NAME": settings.APP_NAME,
        "SHOW_SIDEBAR": show_sidebar(
            request.resolver_match.url_name
            if hasattr(request.resolver_match, "url_name")
            else ""
        ),
    }
