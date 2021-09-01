from typing import Optional

from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest


def show_sidebar(url_name: Optional[str]) -> bool:
    if not url_name:
        return False

    routes = ["guild_view", "channel_"]
    return any(route in url_name for route in routes)


def settings_context(request: WSGIRequest):
    return {
        "DEBUG": settings.DEBUG,
        "APP_NAME": settings.APP_NAME,
        "SHOW_SIDEBAR": show_sidebar(
            request.resolver_match.url_name
            if hasattr(request.resolver_match, "url_name")
            else ""
        ),
    }
