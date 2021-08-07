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

    members = models.ManyToManyField(User)

    def absolute_url(self):
        return reverse("guild:detail", kwargs={"guild_id": str(self.uuid)})

    def members_count(self):
        return self.members.count()

    def save(self, *args, **kwargs):
        self.uuid = uuid.uuid1()

        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)

        if img.size > (128, 128):
            output_size = (128, 128)

            img.thumbnail(output_size)
            img.save(self.avatar.path)

    def __str__(self):
        return "#%d - %s" % (self.uuid or -1, self.name)


class Invite(models.Model):
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE)

    key = models.CharField(max_length=10)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    uses = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse(
            "guild:invite_join",
            kwargs={"guild_id": self.guild.id, "key": self.key},
        )

    def key_url(self):
        return reverse(
            "guild:invite_join",
            kwargs={"guild_id": self.guild.id, "key": self.key},
        )

    def __str__(self):
        return self.get_absolute_url()
