"""
ASGI config for Chat project.
It exposes the ASGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/
"""
import os
import sys
from pathlib import Path

import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

# This allows easy placement of apps within the interior
# Chat directory.
# pylint: disable=import-outside-toplevel
from chat.apps.guilds.features.channels.routing import (  # noqa: E402
    websocket_urlpatterns,
)

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR / "chat"))

# If DJANGO_SETTINGS_MODULE is unset, default to the local settings

# This application object is used by any ASGI server configured
# to use this file.
django_application = get_asgi_application()
# Apply ASGI middleware here.
# from helloworld.asgi import HelloWorldApplication
# application = HelloWorldApplication(application)


application = ProtocolTypeRouter(
    {
        "http": django_application,
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
