from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PagesConfig(AppConfig):
    name = "chat.pages"
    verbose_name = _("Pages")

    def ready(self):
        try:
            # pylint: disable=import-outside-toplevel
            # pylint: disable=unused-import
            import chat.pages.signals  # noqa F401
        except ImportError:
            pass
