# Generated by Django 3.2.8 on 2021-11-06 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="language",
            field=models.CharField(
                choices=[("fr", "Français"), ("en", "English")],
                default="en-us",
                max_length=10,
            ),
        ),
    ]
