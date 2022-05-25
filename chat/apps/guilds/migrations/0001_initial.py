# Generated by Django 3.2.8 on 2022-05-25 12:33

import chat.utils.functions
from django.db import migrations, models
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('filename', models.TextField(blank=True, default=None, null=True)),
                ('file', models.FileField(upload_to=chat.utils.functions.PathAndRename('guilds/attachments'))),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('position', models.IntegerField(default=1)),
                ('name', models.TextField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('position', models.IntegerField(default=1)),
                ('name', models.TextField(max_length=100)),
                ('topic', models.TextField(blank=True, max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Guild',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, verbose_name='Guild Name')),
                ('avatar', models.ImageField(upload_to=chat.utils.functions.PathAndRename('guilds/avatar'), verbose_name='Guild Icon')),
                ('description', models.TextField(blank=True, max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('key', django_extensions.db.fields.RandomCharField(blank=True, editable=False, length=10, unique=True)),
                ('uses', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('attachments', models.ManyToManyField(blank=True, to='guilds.Attachment')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
