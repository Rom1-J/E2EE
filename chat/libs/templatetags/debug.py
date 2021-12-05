import random
import uuid
from datetime import datetime

from django import template
from faker import Faker
from rich import inspect

register = template.Library()
fake = Faker()


@register.filter(name="inspect")
def _inspect(value):
    inspect(value, all=True)

    return value


@register.filter(name="fake_message")
def _fake_message(request):
    def fake_attachments():
        attachments = []

        for _ in range(
            random.choices(
                range(5, 10), weights=[0.6, 0.3, 0.2, 0.05, 0.05], k=1
            )[0]
        ):
            attachments.append(
                {
                    "filename": fake.file_name(),
                    "file": {
                        "url": "dzadzadazdza",
                        "size": random.randint(100, 4000),
                    },
                }
            )

        return attachments

    return {
        "author": random.choice([request.user, None]),
        "id": str(uuid.uuid4()),
        "created_at": datetime.now(),
        "content": fake.paragraph(nb_sentences=5),
        "attachments": fake_attachments(),
    }
