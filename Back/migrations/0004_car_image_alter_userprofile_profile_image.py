# Generated by Django 5.0.4 on 2024-05-14 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Back', '0003_remove_userprofile_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='cars_images/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/'),
        ),
    ]
