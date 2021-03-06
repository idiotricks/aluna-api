# Generated by Django 3.0.3 on 2020-03-22 21:58

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('stocks', '0018_auto_20200321_0151'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockin',
            name='is_in',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='stockout',
            name='is_calculate',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='stockin',
            name='date',
            field=models.DateField(blank=True, default=datetime.date(2020, 3, 22), null=True),
        ),
    ]
