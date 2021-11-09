from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Message


@receiver(post_save, sender=Message)
def on_message_saved(
    sender: Message, instance: Message, **kwargs
):  # pylint: disable=unused-argument
    raise NotImplementedError("Need rework")
    # if channel := instance.channel:
    #     channel.messages.add(instance)
    #     channel.last_message_at = instance.updated_at
    #     channel.save()
    #
    #     if (
    #         len(messages := channel.messages.all()) > 1
    #         and not instance.previous
    #         and instance.same_previous_author is None
    #     ):
    #         if previous := messages.filter(pk__lt=instance.pk).last():
    #             instance.previous = previous
    #             previous.next = instance
    #
    #             instance.same_previous_author = (
    #                 previous.author == instance.author
    #             )
    #             previous.same_next_author = previous.author == instance.author
    #
    #             previous.save()
    #             instance.save()
