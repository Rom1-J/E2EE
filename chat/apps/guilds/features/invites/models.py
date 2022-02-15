import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_extensions.db.fields import RandomCharField

User = get_user_model()


class Invite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    guild = models.ForeignKey("Guild", on_delete=models.CASCADE)

    key = RandomCharField(length=10, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    uses = models.IntegerField(default=0)

    # =========================================================================

    def get_absolute_url(self):
        return reverse(
            "guild:invite_join",
            kwargs={"invite_key": self.key},
        )

    # =========================================================================

    def key_url(self):
        return reverse(
            "guild:invite_join",
            kwargs={"invite_key": self.key},
        )

    # =========================================================================

    def __str__(self):
        return self.get_absolute_url()
