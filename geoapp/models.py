from django.db import models


class GeoData(models.Model):
    address = models.CharField(
        'Адрес',
        max_length=255,
        db_index=True,
        unique=True
    )

    longitude = models.FloatField(
        'Долгота',
        null=True,
        default=None
    )

    latitude = models.FloatField(
        'Широта',
        null=True,
        default=None
    )

    update_time = models.DateTimeField(
        'Дата последнего обновления',
        null=True,
        default=None
    )



