# Generated by Django 3.0.3 on 2020-03-13 10:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0002_auto_20200227_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(default='Ex: Black Tshirt', max_length=100),
        ),
    ]