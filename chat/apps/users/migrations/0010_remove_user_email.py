# Generated by Django 3.2.8 on 2022-05-21 22:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
    ]