from django.http import JsonResponse
from django.templatetags.static import static
import json

from .models import Product, Order, OrderElements


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


def register_order(request):
    try:
        order_information = json.loads(request.body.decode())
    except ValueError:
        return JsonResponse({
            'error': 'bla bla bla',  # TODO fix this
        })

    order, created = Order.objects.get_or_create(
        name=order_information['firstname'],
        surname=order_information['lastname'],
        phonenumber=order_information['phonenumber'],
        address=order_information['address']
    )

    for element in order_information['products']:
        order_details = OrderElements(order=order)
        product_id, quantity = element.values()
        order_details.product = Product.objects.get(id=product_id)
        order_details.quantity = quantity
        order_details.save()

    return JsonResponse({})
