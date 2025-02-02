import requests
from django import forms
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login
from foodcartapp.models import Product, Restaurant, Order
from django.contrib.auth.decorators import user_passes_test
from geopy import distance
from geoapp.models import GeoData
from django.utils import timezone


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, 'login.html', context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect('restaurateur:RestaurantView')
                return redirect('start_page')

        return render(request, 'login.html', context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    default_availability = {restaurant.id: False for restaurant in restaurants}
    products_with_restaurants = []
    for product in products:

        availability = {
            **default_availability,
            **{item.restaurant_id: item.availability for item in product.menu_items.all()},
        }
        orderer_availability = [availability[restaurant.id] for restaurant in restaurants]

        products_with_restaurants.append(
            (product, orderer_availability)
        )

    return render(request, template_name='products_list.html', context={
        'products_with_restaurants': products_with_restaurants,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name='restaurants_list.html', context={
        'restaurants': Restaurant.objects.all(),
    })


def fetch_coordinates(api, address):
    base_url = 'https://geocode-maps.yandex.ru/1.x'
    response = requests.get(base_url, params={
        'geocode': address,
        'apikey': api,
        'format': 'json',
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(' ')
    return lat, lon


def add_distances(order, order_restaurants):
    distances = []
    for restaurant in order_restaurants:
        restaurant.coordinates = (restaurant.geodata.latitude,
                                  restaurant.geodata.longitude)
        distances.append(round(distance.distance((order.geodata.latitude,
                                                  order.geodata.longitude), restaurant.coordinates).km, 2))

    order.rests_with_dists = list(zip(order.restaurants, distances))


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    all_orders = Order.objects.all()
    all_rests = Restaurant.objects.all()
    all_geos = GeoData.objects.all()

    order_addresses = [order.address for order in all_orders]
    rest_addresses = [restaurant.address for restaurant in all_rests]
    all_addresses = set(order_addresses+rest_addresses)

    all_existed_geo_addresses = [geo.address for geo in all_geos]

    need_to_create_addresses = []
    for address in all_addresses:
        if address not in all_existed_geo_addresses:
            need_to_create_addresses.append(address)

    for address in need_to_create_addresses:
        GeoData.objects.create(
            address=address,
            update_time=timezone.now(),

        ).fetch_coordinates()

    order_items = Order.objects.with_price().show_available_rests().with_geo_attributes()
    for order in order_items:
        add_distances(order, order.restaurants)

    return render(request, template_name='order_items.html', context={
            'order_items': order_items,
        })
