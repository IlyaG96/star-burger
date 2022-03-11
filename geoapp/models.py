from django.db import models
import requests
from django.contrib.auth import settings


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

    def fetch_coordinates(self):

        base_url = 'https://geocode-maps.yandex.ru/1.x'
        yandex_api = settings.YANDEX_GEO_API
        response = requests.get(base_url, params={
            'geocode': self.address,
            'apikey': yandex_api,
            'format': 'json',
        })
        response.raise_for_status()
        found_places = response.json()['response']['GeoObjectCollection']['featureMember']

        if not found_places:
            return None

        most_relevant = found_places[0]
        lon, lat = most_relevant['GeoObject']['Point']['pos'].split(' ')
        self.latitude = lat
        self.longitude = lon
        return self.save()
