from django import forms
from django.core.exceptions import ValidationError
from rich import inspect

from .models import Message


class CreateMessageForm(forms.ModelForm):
    class Meta:
        model = Message

        fields = ["author", "channel", "content", "attachments"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cd = self.cleaned_data | self.initial

        channel = cd.get("channel")
        author = cd.get("author")

        if not all((channel, author)):
            raise ValidationError("Internal values not passed")

        if not author.can_see(channel):
            raise ValidationError("Unknown channel for user")

        return cd
