import uuid

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    channels = models.ManyToManyField("Channel", blank=True)
    position = models.PositiveIntegerField(default=0)

    def channels_count(self):
        return self.channels.count()

    def __str__(self):
        return "#%s" % (self.name,)


class Channel(models.Model):
    uuid = models.UUIDField()

    name = models.CharField(max_length=50)
    position = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid1()

        super().save(*args, **kwargs)

    def __str__(self):
        return "#%s - %s" % (self.name, str(self.uuid) or "-1")
