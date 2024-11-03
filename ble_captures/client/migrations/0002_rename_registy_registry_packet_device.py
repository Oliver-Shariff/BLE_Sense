# Generated by Django 5.1.1 on 2024-11-02 03:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Registy',
            new_name='Registry',
        ),
        migrations.AddField(
            model_name='packet',
            name='device',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='packets', to='client.device'),
            preserve_default=False,
        ),
    ]
