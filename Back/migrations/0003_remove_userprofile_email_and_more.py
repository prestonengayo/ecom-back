# Generated by Django 5.0.4 on 2024-04-28 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Back', '0002_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='last_name',
        ),
    ]
