# Generated by Django 5.1.1 on 2024-12-04 01:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='packet',
            name='short_name',
            field=models.TextField(default='d'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='packet',
            name='uuids',
            field=models.TextField(default='d'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='packet',
            name='device',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='packets', to='client.device'),
        ),
        migrations.AlterField(
            model_name='packet',
            name='malicious',
            field=models.BooleanField(default=False),
        ),
    ]