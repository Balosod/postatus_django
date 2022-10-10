from rest_framework import serializers
from .models import (User, Product, Service, Event,
                      Delivery, ProductImages, ServiceImages, EventImages)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
        )
        read_only_fields = ("username",)


class CreateUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "auth_token",
        )
        read_only_fields = ("auth_token",)
        extra_kwargs = {"password": {"write_only": True}}


#Images Serializer
class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
      model = ProductImages
      fields = ['id', 'img']

class ServiceImagesSerializer(serializers.ModelSerializer):
    class Meta:
      model = ServiceImages
      fields = ['id', 'img']

class EventImagesSerializer(serializers.ModelSerializer):
    class Meta:
      model = EventImages
      fields = ['id', 'img']


#Product, Service and Event Serializers with all there images
class ProductSerializer(serializers.ModelSerializer):
    posts = ProductImagesSerializer(many=True)

    class Meta:
        model = Product
        fields = ['what_to_sell','quantity','category','location','price','description','tags','posts']

class ServiceSerializer(serializers.ModelSerializer):
    posts = ServiceImagesSerializer(many=True)

    class Meta:
        model = Service
        fields = ['what_to_do','delivery_type','duration','category','location','price','description','tags','posts']

class EventSerializer(serializers.ModelSerializer):
    posts = EventImagesSerializer(many=True)

    class Meta:
        model = Event
        fields = ['what_is_it_about','medium','date_and_time','category','location','price','description','tags','posts']

# class DeliveryOutSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Delivery
#         fields = '_all_'


# All Product, Service and Event Serializers
class ProductServiceEventSerializer(serializers.Serializer):
    product = ProductSerializer(many = True)
    service = ServiceSerializer(many=True)
    event = EventSerializer(many=True)
