# Generated by Django 2.2.1 on 2019-05-10 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruitsandjuice', '0004_product_unit_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sale',
            field=models.BooleanField(default=False),
        ),
    ]
