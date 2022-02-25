from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from foodcartapp.models import Order, OrderElements
from rest_framework.serializers import ValidationError


class OrderElementsSerializer(ModelSerializer):

    def create(self, validated_data):
        return OrderElements.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.product = validated_data.get('product', instance.product)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()

        return instance

    class Meta:
        model = OrderElements
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):

    products = OrderElementsSerializer(many=True, allow_null=False)

    def validate_products(self, products):
        if not products:
            raise ValidationError('products: список не может быть пустым')
        return products

    class Meta:
        model = Order
        fields = ['id', 'firstname', 'lastname', 'phonenumber', 'address', 'products']

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.firstname = validated_data.get('name', instance.name)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.phonenumber = validated_data.get('phonenumber', instance.phonenumber)
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        return instance














