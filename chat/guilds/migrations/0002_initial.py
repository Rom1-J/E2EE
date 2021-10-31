# Generated by Django 3.2.6 on 2021-10-31 16:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('guilds', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='channel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='guilds.channel'),
        ),
        migrations.AddField(
            model_name='message',
            name='next',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_message', to='guilds.message'),
        ),
        migrations.AddField(
            model_name='message',
            name='previous',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='previous_message', to='guilds.message'),
        ),
        migrations.AddField(
            model_name='invite',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='invite',
            name='guild',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guilds.guild'),
        ),
        migrations.AddField(
            model_name='guild',
            name='channels',
            field=models.ManyToManyField(blank=True, related_name='channels', to='guilds.Channel'),
        ),
        migrations.AddField(
            model_name='guild',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='guild',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='channel',
            name='guild',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='guilds.guild'),
        ),
        migrations.AddField(
            model_name='channel',
            name='last_message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_message', to='guilds.message'),
        ),
        migrations.AddField(
            model_name='channel',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='guilds.channel'),
        ),
    ]
