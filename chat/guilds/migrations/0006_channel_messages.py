# Generated by Django 3.2.6 on 2021-08-10 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("guilds", "0005_auto_20210810_1430"),
    ]

    operations = [
        migrations.AddField(
            model_name="channel",
            name="messages",
            field=models.ManyToManyField(to="guilds.Message"),
        ),
    ]