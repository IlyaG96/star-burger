from rest_framework.serializers import ModelSerializer
from foodcartapp.models import Order, OrderElements
from rest_framework.serializers import ValidationError


class OrderElementsSerializer(ModelSerializer):

    class Meta:
        model = OrderElements
        fields = ['product', 'quantity']

    def create(self, validated_data):
        return OrderElements.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return OrderElements.objects.update(**validated_data)


class OrderSerializer(ModelSerializer):

    products = OrderElementsSerializer(many=True, allow_null=False, write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'firstname', 'lastname', 'phonenumber', 'address', 'products']

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return Order.objects.update(**validated_data)

    def validate_products(self, products):
        if not products:
            raise ValidationError('products: список не может быть пустым')
        return products
