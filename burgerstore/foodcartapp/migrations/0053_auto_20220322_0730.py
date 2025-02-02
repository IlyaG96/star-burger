# Generated by Django 3.2 on 2022-03-22 07:30

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0052_alter_order_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderelements',
            name='price_in_order',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Стоимость'),
        ),
        migrations.AlterField(
            model_name='orderelements',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_elements', to='foodcartapp.product', verbose_name='Продукт'),
        ),
        migrations.AlterField(
            model_name='orderelements',
            name='quantity',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество'),
        ),
    ]
