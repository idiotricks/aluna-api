# Generated by Django 3.0.3 on 2020-03-22 22:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0010_remove_supplier_is_publish'),
        ('stocks', '0021_auto_20200323_0503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockout',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='supplierstockout', to='users.Customer'),
        ),
    ]
