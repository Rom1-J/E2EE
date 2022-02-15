from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GuildsConfig(AppConfig):
    name = "chat.apps.guilds"
    verbose_name = _("Guilds")

    def ready(self):
        try:
            # pylint: disable=import-outside-toplevel
            # pylint: disable=unused-import
            import chat.apps.guilds.signals  # noqa F401
        except ImportError:
            pass
