# Generated by Django 5.1.1 on 2024-11-25 16:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0007_user'),
        ('collection', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='systeminfo',
            name='scanner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='client.scanner'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='systeminfo',
            name='timestamp',
            field=models.DateTimeField(default='2024-11-25 14:30:00'),
            preserve_default=False,
        ),
    ]