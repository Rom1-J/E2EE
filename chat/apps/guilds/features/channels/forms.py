from django import forms
from rich import inspect

from .models import Message


class CreateMessageForm(forms.ModelForm):
    class Meta:
        model = Message

        fields = ["content", "attachments"]

    def __init__(self, *args, **kwargs):
        inspect(args)
        inspect(kwargs)

        super().__init__(*args, **kwargs)
