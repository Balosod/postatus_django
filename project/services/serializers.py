from rest_framework import serializers
from .models import (Product, Service, Event,Delivery, ProductImages, 
                     ServiceImages, EventImages)


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
        fields = ['id','what_to_sell','quantity','category','location','price','description','tags','owner','posts']

class ServiceSerializer(serializers.ModelSerializer):
    posts = ServiceImagesSerializer(many=True,read_only=True)

    class Meta:
        model = Service
        fields = ['id','what_to_do','delivery_type','duration','category','location','price','description','tags','owner','posts']

class EventSerializer(serializers.ModelSerializer):
    posts = EventImagesSerializer(many=True,read_only=True)

    class Meta:
        model = Event
        fields = ['id','what_is_it_about','medium','date_and_time','category','location','price','description','tags','owner','posts']

#Delivery Serializer
class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['id','pick_up_location','delivery_location','category','delivery_type','size','select_category','price','description','tags','owner']


# All Product, Service and Event Serializer
class ProductServiceEventSerializer(serializers.Serializer):
    product = ProductSerializer(many = True)
    service = ServiceSerializer(many=True)
    event = EventSerializer(many=True)
    delivery = DeliverySerializer(many=True)
