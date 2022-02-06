"""
ASGI config for Chat project.
It exposes the ASGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/
"""
import os
import sys
from pathlib import Path

import channels.routing
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

# This allows easy placement of apps within the interior
# Chat directory.
import chat.guilds.features.channels.routing

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR / "chat"))

# If DJANGO_SETTINGS_MODULE is unset, default to the local settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

# This application object is used by any ASGI server configured
# to use this file.
django_application = get_asgi_application()
# Apply ASGI middleware here.
# from helloworld.asgi import HelloWorldApplication
# application = HelloWorldApplication(application)


application = channels.routing.ProtocolTypeRouter(
    {
        "http": django_application,
        "websocket": AuthMiddlewareStack(
            channels.routing.URLRouter(
                chat.guilds.features.channels.routing.websocket_urlpatterns
            )
        ),
    }
)
