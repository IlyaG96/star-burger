# Generated by Django 3.2 on 2022-02-25 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0041_auto_20220223_1038'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='surname',
            new_name='lastname',
        ),
    ]
