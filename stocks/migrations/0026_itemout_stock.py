# Generated by Django 3.0.3 on 2020-03-29 14:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('stocks', '0025_auto_20200329_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemout',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
    ]