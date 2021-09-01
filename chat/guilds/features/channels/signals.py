from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Message


@receiver(post_save, sender=Message)
def on_message_saved(
    sender: Message, instance: Message, **kwargs
):  # pylint: disable=unused-argument
    if channel := instance.channel:
        channel.messages.add(instance)
        channel.last_message_at = instance.updated_at
        channel.save()
