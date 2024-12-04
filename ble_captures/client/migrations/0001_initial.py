# Generated by Django 5.1.1 on 2024-12-02 19:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('user_name', models.TextField()),
                ('user_password', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Registry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.TextField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registries', to='client.company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registries', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Scanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scanners', to='client.company')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scanners', to='client.group')),
            ],
        ),
        migrations.CreateModel(
            name='Packet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advertising_address', models.TextField()),
                ('power_level', models.FloatField()),
                ('company_id', models.TextField()),
                ('time_stamp', models.DateField()),
                ('rssi', models.IntegerField()),
                ('channel_index', models.IntegerField()),
                ('counter', models.IntegerField()),
                ('protocol_version', models.IntegerField()),
                ('malicious', models.BooleanField()),
                ('long_name', models.TextField()),
                ('oui', models.TextField()),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packets', to='client.device')),
                ('scanner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.scanner')),
            ],
        ),
        migrations.CreateModel(
            name='Heartbeat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('used_mem', models.FloatField()),
                ('total_mem', models.FloatField()),
                ('used_swap', models.FloatField()),
                ('total_swap', models.FloatField()),
                ('serial_num', models.IntegerField()),
                ('timestamp', models.DateField()),
                ('total_cpu', models.FloatField()),
                ('disk_info', models.TextField()),
                ('queue_length', models.IntegerField()),
                ('scanner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.scanner')),
            ],
        ),
        migrations.CreateModel(
            name='Scans',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('packet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.packet')),
                ('scanner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.scanner')),
            ],
        ),
        migrations.CreateModel(
            name='Uuid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.IntegerField()),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.device')),
            ],
        ),
    ]