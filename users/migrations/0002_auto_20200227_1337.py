# Generated by Django 3.0.3 on 2020-02-27 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='code_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
