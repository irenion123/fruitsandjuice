# Generated by Django 2.2.1 on 2019-05-25 10:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fruitsandjuice', '0006_productcategory_anchor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=25, verbose_name='Моб. телефон')),
                ('payment_method', models.CharField(choices=[('CH', 'Наличными'), ('NCH', 'Безналичные')], default='CH', max_length=3, verbose_name='Способ оплаты')),
                ('delivery_method', models.CharField(choices=[('PU', 'Самовывоз'), ('CR', 'Курьером')], default='CR', max_length=3, verbose_name='Способ доставки')),
                ('adress', models.CharField(blank=True, max_length=50, null=True, verbose_name='Адрес')),
                ('status', models.CharField(choices=[('FM', 'Формируется'), ('ACP', 'Оформлен'), ('INP', 'Собирается'), ('RDY', 'Готов к выдаче'), ('DTS', 'Отдан в службу доставки'), ('CNC', 'Отменён'), ('ISU', 'Выдан')], default='FM', max_length=3, verbose_name='Статус')),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fruitsandjuice.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='fruitsandjuice.Product')),
            ],
        ),
    ]