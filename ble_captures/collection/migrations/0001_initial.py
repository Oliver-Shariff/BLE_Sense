# Generated by Django 5.1.1 on 2024-12-04 15:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_memory', models.FloatField()),
                ('used_memory', models.FloatField()),
                ('total_swap', models.FloatField()),
                ('used_swap', models.FloatField()),
                ('total_cpu_usage', models.FloatField()),
                ('disk_info', models.TextField()),
                ('packet_queue_length', models.IntegerField()),
                ('timestamp', models.DateField()),
                ('scanner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.scanner')),
            ],
        ),
        migrations.CreateModel(
            name='NetworkInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interface_name', models.TextField()),
                ('total_received', models.IntegerField()),
                ('total_transmitted', models.IntegerField()),
                ('system_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='network_information', to='collection.systeminfo')),
            ],
        ),
    ]
