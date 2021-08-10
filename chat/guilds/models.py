import uuid

from PIL import Image
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from chat.users.models import User


class Guild(models.Model):
    uuid = models.UUIDField()

    name = models.CharField(_("Guild Name"), max_length=42)
    avatar = models.ImageField(_("Guild Avatar"))

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner"
    )

    members = models.ManyToManyField(User)

    channels = models.ManyToManyField("Channel", blank=True)
    categories = models.ManyToManyField("Category", blank=True)

    # =========================================================================

    def get_absolute_url(self):
        return reverse("guild:guild_view", kwargs={"guild_id": str(self.uuid)})

    # =========================================================================

    def members_count(self):
        return self.members.count()

    def channels_count(self):
        return self.categories.count() + sum(
            [category.channels_count() for category in self.categories.all()]
        )

    def categories_count(self):
        return self.categories.count()

    # =========================================================================

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid1()

        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)

        if img.size > (128, 128):
            output_size = (128, 128)

            img.thumbnail(output_size)
            img.save(self.avatar.path)

    def __str__(self):
        return "#%s - %s" % (self.name, str(self.uuid) or "-1")


# =============================================================================
