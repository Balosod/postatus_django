from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from project.services import models
from project.services.serializers import (ProductServiceEventSerializer,ProductSerializer,EventImagesSerializer,
                             DeliverySerializer)

from tagging.models import TaggedItem
from tagging.models import Tag
from collections import namedtuple
Item = namedtuple('Item', ('product', 'service','event','delivery'))

# Create your views here.


class Explore(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        item = Item(product = models.Product.objects.all(),
                        service = models.Service.objects.all(),
                        event = models.Event.objects.all(),
                        delivery = models.Delivery.objects.all())
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
            query_set = TaggedItem.objects.get_by_model(models.Product, tag)
            serializer = ProductSerializer(query_set,many=True)
            output_data.append(serializer.data[0])
        except:
            pass
        try:
            query_set = TaggedItem.objects.get_by_model(models.Service, tag)
            serializer = ServiceSerializer(query_set,many=True)
            output_data.append(serializer.data[0])
        except:
            pass
        try:
            query_set = TaggedItem.objects.get_by_model(models.Event, tag)
            serializer = EventSerializer(query_set,many=True)
            output_data.append(serializer.data[0])
        except:
            pass
        try:
            query_set = TaggedItem.objects.get_by_model(models.Delivery, tag)
            serializer = DeliverySerializer(query_set,many=True)
            output_data.append(serializer.data[0])
        except:
            pass
        if output_data:
            return Response(output_data, status=status.HTTP_200_OK)
        else:
            return Response('No match',status=status.HTTP_400_BAD_REQUEST)