from rest_framework import serializers
from foodcartapp.models import Order, OrderElements, Product
from phonenumber_field.serializerfields import PhoneNumberField


class OrderSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    firstname = serializers.CharField(max_length=100, required=True)
    lastname = serializers.CharField(max_length=100, required=True)
    phonenumber = PhoneNumberField(required=True)
    address = serializers.CharField(max_length=255, required=True)

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.firstname = validated_data.get('name', instance.name)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.phonenumber = validated_data.get('phonenumber', instance.phonenumber)
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        return instance


class OrderElementsSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    product = serializers.SlugRelatedField(required=True,
                                           slug_field='id',
                                           queryset=Product.objects,
                                           allow_empty=False)
    quantity = serializers.IntegerField(required=True,
                                        min_value=1,
                                        allow_null=False)

    def create(self, validated_data):
        return OrderElements.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.product = validated_data.get('product', instance.product)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()

        return instance











