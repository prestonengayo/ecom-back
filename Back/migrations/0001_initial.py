# Generated by Django 5.0.4 on 2024-04-25 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('brand', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('color', models.CharField(max_length=50)),
                ('gearbox', models.CharField(choices=[('manual', 'Manual'), ('automatic', 'Automatic')], default='manual', max_length=10)),
                ('engine_type', models.CharField(choices=[('electric', 'Electric'), ('mechanical', 'Mechanical'), ('hybrid', 'Hybrid')], default='mechanical', max_length=10)),
            ],
        ),
    ]
