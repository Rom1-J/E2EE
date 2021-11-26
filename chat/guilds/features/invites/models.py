import uuid

from django.db import models
from django.urls import reverse

from chat.users.models import User


class Invite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    guild = models.ForeignKey("Guild", on_delete=models.CASCADE)

    key = models.CharField(max_length=10)
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
