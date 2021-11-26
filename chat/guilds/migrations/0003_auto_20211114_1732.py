# Generated by Django 3.2.8 on 2021-11-14 17:32

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('guilds', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channel',
            name='type',
        ),
        migrations.AlterField(
            model_name='channel',
            name='position',
            field=models.IntegerField(default=1),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('position', models.IntegerField(default=1)),
                ('name', models.TextField(max_length=100)),
                ('guild', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='guilds.guild')),
            ],
        ),
        migrations.AlterField(
            model_name='channel',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='guilds.category'),
        ),
    ]