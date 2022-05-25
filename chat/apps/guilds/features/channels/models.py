import os
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from chat.utils.functions import PathAndRename, remove_exif

User = get_user_model()


class Category(models.Model):
    class Meta:
        verbose_name_plural = _("Categories")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    guild = models.ForeignKey(
        "Guild", on_delete=models.CASCADE, blank=True, null=True
    )

    position = models.IntegerField(default=1)

    name = models.TextField(max_length=100)

    # =========================================================================

    def get_channels(self):
        return Channel.objects.filter(parent=self)

    def channels_count(self):
        return len(self.get_channels().all())

    # =========================================================================

    def __str__(self):
        return f"{self.name}"


# =============================================================================


class Channel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    guild = models.ForeignKey(
        "Guild",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    position = models.IntegerField(default=1)
    parent = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, default=None, blank=True, null=True
    )

    name = models.TextField(max_length=100)
    topic = models.TextField(max_length=1024, blank=True, null=True)

    # =========================================================================

    def get_messages(self, recipient: User):
        return Message.objects.filter(channel=self, recipient=recipient)

    # =========================================================================

    def __str__(self):
        return f"#{self.name}"


# =============================================================================
# =============================================================================


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    channel = models.ForeignKey(
        "Channel",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    content = models.TextField()
    nonce = models.TextField()

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author"
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipient"
    )

    attachments = models.ManyToManyField("Attachment", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    # =========================================================================

    def __str__(self):
        return (
            f"from: {self.author}, "
            f"to: {self.recipient}, "
            f"id: {self.id}, "
        )


# =============================================================================
# =============================================================================


class Attachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    filename = models.TextField(null=True, blank=True, default=None)

    file = models.FileField(upload_to=PathAndRename("guilds/attachments"))

    # =========================================================================

    def extension(self):
        return self.file.name.split(".")[-1]

    # =========================================================================

    def save(self, *args, **kwargs):
        if not self.filename:
            self.filename = os.path.basename(self.file.name)

        super().save(*args, **kwargs)

        if cleaned := remove_exif(self.file.path):
            cleaned.save(self.file.path)

    def __str__(self):
        return f"file: {self.id}"
