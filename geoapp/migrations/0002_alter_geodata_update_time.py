# Generated by Django 3.2 on 2022-03-22 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geoapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geodata',
            name='update_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата последнего обновления'),
        ),
    ]
