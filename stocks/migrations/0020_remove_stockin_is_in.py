# Generated by Django 3.0.3 on 2020-03-22 22:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('stocks', '0019_auto_20200323_0458'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockin',
            name='is_in',
        ),
    ]
