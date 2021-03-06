# Generated by Django 3.0.3 on 2020-03-18 08:32

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0008_auto_20200314_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='created_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='updated_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='supplier',
            name='created_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='supplier',
            name='updated_date',
            field=models.DateField(auto_now=True),
        ),
    ]
