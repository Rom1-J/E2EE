from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GroupsConfig(AppConfig):
    name = "chat.guild"
    verbose_name = _("Guilds")

    def ready(self):
        try:
            # pylint: disable=import-outside-toplevel
            # pylint: disable=unused-import
            import chat.guild.signals  # noqa F401
        except ImportError:
            pass
