from rest_framework import serializers
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from .models import (User, Product, Service, Event,Delivery, ProductImages, 
                     ServiceImages, EventImages,Interest)
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "interests",
        )
        read_only_fields = ("username",)


# class CreateUserSerializer(serializers.ModelSerializer):
#     def create(self, validated_data):
#         # call create_user on user object. Without this
#         # the password will be stored in plain text.
#         user = User.objects.create_user(**validated_data)
#         return user

#     class Meta:
#         model = User
#         fields = (
#             "id",
#             "username",
#             "password",
#             "first_name",
#             "last_name",
#             "email",
#             "auth_token",
#         )
#         read_only_fields = ("auth_token",)
#         extra_kwargs = {"password": {"write_only": True}}

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
      model = Interest
      fields = ['id','name']


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta:
        model = User
        fields = ('id', 'email','password','interests',)
    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")
        return user

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


#Product, Service and Event Serializer with all there images
class ProductSerializer(serializers.ModelSerializer):
    posts = ProductImagesSerializer(many=True,read_only=True)

    class Meta:
        model = Product
        fields = ['what_to_sell','quantity','category','location','price','description','tags','owner','posts']

class ServiceSerializer(serializers.ModelSerializer):
    posts = ServiceImagesSerializer(many=True,read_only=True)

    class Meta:
        model = Service
        fields = ['what_to_do','delivery_type','duration','category','location','price','description','tags','owner','posts']

class EventSerializer(serializers.ModelSerializer):
    posts = EventImagesSerializer(many=True,read_only=True)

    class Meta:
        model = Event
        fields = ['what_is_it_about','medium','date_and_time','category','location','price','description','tags','owner','posts']

#Delivery Serializer
class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'


# All Product, Service and Event Serializer
class ProductServiceEventSerializer(serializers.Serializer):
    product = ProductSerializer(many = True)
    service = ServiceSerializer(many=True)
    event = EventSerializer(many=True)
