import uuid

from PIL import Image
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from chat.utils.functions import PathAndRename


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    avatar = models.ImageField(
        upload_to=PathAndRename("users/avatar"), blank=True, null=True
    )

    bio = models.TextField(max_length=1000, blank=True, null=True)

    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = None  # type: ignore

    language = models.CharField(
        max_length=10,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE,
    )

    first_connect = models.BooleanField(default=True)
    mnemonic = models.CharField(max_length=255, blank=True, null=True)

    # =========================================================================

    USERNAME_FIELD = "username"

    # =========================================================================

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar:
            img = Image.open(self.avatar.path)

            if img.size > (128, 128):
                output_size = (128, 128)

                img.thumbnail(output_size)
                img.save(self.avatar.path)

    # =========================================================================

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    # =========================================================================

    def __str__(self):
        return str(self.username if self.username else self.id)


# =============================================================================
