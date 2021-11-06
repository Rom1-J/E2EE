import uuid

from PIL import Image
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    uuid = models.UUIDField()

    email = models.EmailField(_("User's email"), max_length=255, unique=True)
    avatar = models.ImageField(upload_to="avatars", blank=True, null=True)

    bio = models.TextField(max_length=1000, blank=True, null=True)

    first_name = None
    last_name = None

    language = models.CharField(
        max_length=10,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE
    )

    # =========================================================================

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    # =========================================================================

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()

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
        return "%s" % (self.username if self.username else self.uuid)

# =============================================================================
