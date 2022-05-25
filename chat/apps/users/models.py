import uuid
from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image

from chat.utils.functions import PathAndRename

if TYPE_CHECKING:
    from chat.apps.guilds.features.channels.models import Channel


class UserSettings(models.Model):
    class Theme(models.TextChoices):
        DARK = "DK", _("Dark")
        LIGHT = "LT", _("Light")

    class Meta:
        verbose_name_plural = _("User Settings")

    # =========================================================================

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    language = models.CharField(
        max_length=10,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE,
    )

    theme = models.CharField(
        max_length=2, choices=Theme.choices, default=Theme.DARK
    )

    avatar = models.ImageField(
        upload_to=PathAndRename("users/avatar"), blank=True, null=True
    )

    bio = models.TextField(max_length=1000, blank=True, null=True)

    collapsed_categories = models.ManyToManyField(
        "guilds.Category", default=None, blank=True
    )

    # =========================================================================

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar:
            img = Image.open(self.avatar.path)

            if img.size > (128, 128):
                output_size = (128, 128)

                img.thumbnail(output_size)
                img.save(self.avatar.path)


# =============================================================================


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    settings = models.ForeignKey(
        UserSettings,
        on_delete=models.SET_NULL,
        related_name="user_settings",
        blank=True,
        null=True,
    )

    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = None  # type: ignore
    # email = models.EmailField(unique=True, blank=True, null=True)  # None  # type: ignore

    first_connect = models.BooleanField(default=True)

    mnemonic = models.CharField(max_length=255, blank=True, null=True)
    public_key = models.CharField(max_length=255, blank=True, null=True)

    # =========================================================================

    USERNAME_FIELD = "username"

    # =========================================================================

    def save(self, *args, **kwargs):
        if not self.settings:
            user_settings = UserSettings()
            user_settings.save()

            self.settings = user_settings

        super().save(*args, **kwargs)

    # =========================================================================

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    # =========================================================================

    def can_see(self, channel: "Channel") -> bool:
        """Return either the user can see the channel or not"""

        return self in channel.guild.members.all()

    # =========================================================================

    def __str__(self):
        return str(self.username if self.username else self.id)


# =============================================================================
