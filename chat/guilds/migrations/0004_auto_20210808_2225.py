# Generated by Django 3.1.13 on 2021-08-08 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("guilds", "0003_auto_20210808_2154"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="channels",
            field=models.ManyToManyField(blank=True, to="guilds.Channel"),
        ),
    ]
