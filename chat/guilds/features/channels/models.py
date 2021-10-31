import os
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from chat.users.models import User

from .utils import remove_exif, rename_file


class Channel(models.Model):
    class ChannelType(models.TextChoices):
        DM = "DM", _("Direct Message")
        GROUP_DM = "GROUP_DM", _("Group Direct Message")

        TEXT = "TEXT", _("Text")
        CATEGORY = "CATEGORY", _("Category")
        NEWS = "NEWS", _("News")

    uuid = models.UUIDField()

    type = models.CharField(
        max_length=10,
        choices=ChannelType.choices,
    )

    guild = models.ForeignKey(
        "Guild",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    position = models.IntegerField()
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    name = models.TextField(max_length=100)
    topic = models.TextField(max_length=1024, blank=True, null=True)

    last_message = models.ForeignKey(
        "Message",
        on_delete=models.SET_NULL,
        related_name="last_message",
        blank=True,
        null=True
    )

    # =========================================================================

    def message_count(self):
        return 42

    # =========================================================================

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid1()

        super().save(*args, **kwargs)

    def __str__(self):
        return "#%s - %s" % (self.name, str(self.uuid) or "-1")


# =============================================================================
# =============================================================================


class Message(models.Model):
    uuid = models.UUIDField()

    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
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


# =============================================================================
# =============================================================================


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
