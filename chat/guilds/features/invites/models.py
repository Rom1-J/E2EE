from django.urls import reverse
from django.db import models

from chat.users.models import User
from ...models import Guild


class Invite(models.Model):
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE)

    key = models.CharField(max_length=10)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    uses = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse(
            "guild:invite_join",
            kwargs={"invite_key": self.key},
        )

    def key_url(self):
        return reverse(
            "guild:invite_join",
            kwargs={"invite_key": self.key},
        )

    def __str__(self):
        return self.get_absolute_url()
