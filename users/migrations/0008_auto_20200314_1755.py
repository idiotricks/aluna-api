# Generated by Django 3.0.3 on 2020-03-14 10:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0007_supplier_is_init'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='is_publish',
        ),
        migrations.AddField(
            model_name='customer',
            name='is_init',
            field=models.BooleanField(default=True),
        ),
    ]
