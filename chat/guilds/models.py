import uuid

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image

from chat.users.models import User

from ..utils.functions import PathAndRename
from .features.channels.models import Channel


class Guild(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(_("Guild Name"), max_length=200)
    avatar = models.ImageField(
        _("Guild Icon"), upload_to=PathAndRename("guilds/avatar")
    )

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner"
    )

    members = models.ManyToManyField(User)
    bans = models.ManyToManyField(User, related_name="bans")
    channels = models.ManyToManyField(
        Channel, blank=True, related_name="channels"
    )

    description = models.TextField(max_length=1024, blank=True, null=True)

    # =========================================================================

    def get_absolute_url(self):
        return reverse(
            "guild:guild_details", kwargs={"guild_id": str(self.id)}
        )

    # =========================================================================

    def members_count(self):
        return self.members.count()

    # =========================================================================

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)

        if img.size > (128, 128):
            output_size = (128, 128)

            img.thumbnail(output_size)
            img.save(self.avatar.path)

    def __str__(self):
        return f"#{self.name} - {self.id or '-1'}"


# =============================================================================
