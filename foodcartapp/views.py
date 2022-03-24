from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from .serializers import OrderSerializer
from .models import Product, Order, OrderElements
from rest_framework.response import Response
from django.db import transaction
from geoapp.models import GeoData
from django.utils import timezone
from textwrap import dedent


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            },
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@transaction.atomic
@api_view(['POST'])
def register_order(request):
    order_serializer = OrderSerializer(data=request.data)
    order_serializer.is_valid(raise_exception=True)
    order = Order.objects.create(
        firstname=order_serializer.validated_data['firstname'],
        lastname=order_serializer.validated_data['lastname'],
        phonenumber=order_serializer.validated_data['phonenumber'],
        address=order_serializer.validated_data['address']
    )
    current_address, created = GeoData.objects.get_or_create(
        address=order_serializer.validated_data['address'],
    )

    if created:
        GeoData.fetch_coordinates(current_address)

    for element in order_serializer.validated_data['products']:
        product, quantity = element.values()
        OrderElements.objects.create(order=order,
                                     product=product,
                                     quantity=quantity,
                                     price_in_order=product.price * quantity)

    return Response({
        dedent(f'''
        Заказ {order.id} на адрес {order.address} создан.
        ''')

    })


@api_view(['GET'])
def view_order(request, order_id):

    order = Order.objects.get(id=order_id)
    order_serializer = OrderSerializer(order)

    return Response(order_serializer.data)
