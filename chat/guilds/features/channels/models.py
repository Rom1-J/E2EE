import os
import uuid

from django.db import models

from chat.users.models import User

from .utils import remove_exif, rename_file


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

    messages = models.ManyToManyField("Message", related_name="messages")

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

    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name="channel",
        blank=True,
        null=True,
    )

    content = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author"
    )

    attachments = models.ManyToManyField("Attachment", blank=True)

    previous = models.OneToOneField(
        "self",
        null=True,
        blank=True,
        related_name="previous_message",
        on_delete=models.SET_NULL,
    )
    same_previous_author = models.BooleanField(blank=True, null=True)

    next = models.OneToOneField(
        "self",
        null=True,
        blank=True,
        related_name="next_message",
        on_delete=models.SET_NULL,
    )
    same_next_author = models.BooleanField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    # =========================================================================

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid1()

        super().save(*args, **kwargs)

    def __str__(self):
        return "from: %s, " \
               "uuid: %s, " \
               "same_previous_author: %s, " \
               "same_next_author: %s" % (
            str(self.author),
            str(self.uuid),
            str(self.same_previous_author),
            str(self.same_next_author),
        )


class Attachment(models.Model):
    uuid = models.UUIDField()

    filename = models.TextField(null=True, blank=True, default=None)

    file = models.FileField(upload_to=rename_file)

    # =========================================================================

    def extension(self):
        return self.file.name.split(".")[-1]

    # =========================================================================

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid1()

        if not self.filename:
            self.filename = os.path.basename(self.file.name)

        super().save(*args, **kwargs)

        if cleaned := remove_exif(self.file.path):
            cleaned.save(self.file.path)

    def __str__(self):
        return "file: %s" % (str(self.uuid),)
