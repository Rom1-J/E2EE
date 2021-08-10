import uuid

from django.db import models

from chat.users.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)

    channels = models.ManyToManyField("Channel", blank=True)
    position = models.PositiveIntegerField(default=0)

    # =========================================================================

    def channels_count(self):
        return self.channels.count()

    # =========================================================================

    def __str__(self):
        return "#%s" % (self.name,)


class Channel(models.Model):
    uuid = models.UUIDField()

    name = models.CharField(max_length=50)
    position = models.PositiveIntegerField(default=0)

    last_message_at = models.DateTimeField(blank=True, null=True, default=None)

    messages = models.ManyToManyField("Message")

    # =========================================================================

    def messages_count(self):
        return self.messages.count()

    # =========================================================================

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid1()

        super().save(*args, **kwargs)

    def __str__(self):
        return "#%s - %s" % (self.name, str(self.uuid) or "-1")


class Message(models.Model):
    uuid = models.UUIDField()

    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # =========================================================================

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid1()

        if channel := self.channel_set.first():
            channel.last_message_at = self.updated_at

        super().save(*args, **kwargs)

    def __str__(self):
        return "from: %s" % (str(self.author),)
