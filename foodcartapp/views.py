from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from .serializers import OrderSerializer, OrderElementsSerializer
from .models import Product, Order, OrderElements
from rest_framework.response import Response
from rest_framework.serializers import ValidationError


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


@api_view(['POST'])
def register_order(request):

    order_information = request.data

    order_serializer = OrderSerializer(data=order_information, required=True)

    try:
        order_elements_serializer = OrderElementsSerializer(data=order_information['products'],
                                                            many=True)

    except KeyError:
        raise ValidationError(["products: Обязательное поле"])

    if not order_information['products']:
        raise ValidationError(["products: список не может быть пустым"])

    if order_serializer.is_valid(raise_exception=True):
        if order_elements_serializer.is_valid(raise_exception=True):

            order = Order.objects.create(
                firstname=order_information['firstname'],
                lastname=order_information['lastname'],
                phonenumber=order_information['phonenumber'],
                address=order_information['address']
            )

            for element in order_information['products']:
                if not element:
                    raise ValidationError(["products: Этот список не может быть пустым."])

                order_details = OrderElements(order=order)
                product_id, quantity = element.values()
                order_details.product = Product.objects.get(id=product_id)
                order_details.quantity = quantity
                order_details.save()

    return Response({})
