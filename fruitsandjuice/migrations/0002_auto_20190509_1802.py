# Generated by Django 2.2.1 on 2019-05-09 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruitsandjuice', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitsProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, verbose_name='Единица товара')),
            ],
            options={
                'verbose_name': 'Единица товара',
                'verbose_name_plural': 'Единицы товара',
            },
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name': 'Страна', 'verbose_name_plural': 'Страны'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
    ]
