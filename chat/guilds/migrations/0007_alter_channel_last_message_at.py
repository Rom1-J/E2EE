# Generated by Django 3.2.6 on 2021-08-10 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("guilds", "0006_channel_messages"),
    ]

    operations = [
        migrations.AlterField(
            model_name="channel",
            name="last_message_at",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
