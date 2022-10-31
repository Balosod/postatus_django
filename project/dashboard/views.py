from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from project.services import models
from project.services.serializers import (ProductServiceEventSerializer,ServiceSerializer,ProductSerializer,EventImagesSerializer,
                             DeliverySerializer)
from rest_framework.permissions import IsAuthenticated
from tagging.models import TaggedItem
from tagging.models import Tag
from collections import namedtuple
Item = namedtuple('Item', ('product', 'service','event','delivery'))

# Create your views here.

class Dashboard(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        item = Item(product = models.Product.objects.filter(owner = request.user.id),
                    service = models.Service.objects.filter(owner = request.user.id),
                    event = models.Event.objects.filter(owner = request.user.id),
                    delivery = models.Delivery.objects.filter(owner = request.user.id))
        serializer = ProductServiceEventSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request):
        output_data = []
        data = request.data
        input_tag = data["input_tag"]
        try:
            tag = Tag.objects.get(name=input_tag)
        except:
            return Response('Tags does not exist',status=status.HTTP_400_BAD_REQUEST)
        try:
            product = models.Product.objects.filter(owner = request.user.id)
            query_set = TaggedItem.objects.get_by_model(product, tag)
            serializer = ProductSerializer(query_set,many=True)
            output_data.extend(serializer.data)
        except:
            pass
        try:
            service = models.Service.objects.filter(owner = request.user.id)
            query_set = TaggedItem.objects.get_by_model(service, tag)
            serializer = ServiceSerializer(query_set,many=True)
            output_data.extend(serializer.data)
        except:
            pass
        try:
            event = models.Event.objects.filter(owner = request.user.id)
            query_set = TaggedItem.objects.get_by_model(event, tag)
            serializer = EventSerializer(query_set,many=True)
            output_data.extend(serializer.data)
        except:
            pass
        try:
            delivery = models.Delivery.objects.filter(owner = request.user.id)
            query_set = TaggedItem.objects.get_by_model(delivery, tag)
            serializer = DeliverySerializer(query_set,many=True)
            output_data.extend(serializer.data)
        except:
            pass
        if output_data:
            return Response(output_data, status=status.HTTP_200_OK)
        else:
            return Response('No match',status=status.HTTP_400_BAD_REQUEST)