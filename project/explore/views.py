from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from project.services import models
from project.services.serializers import (ProductServiceEventSerializer,ServiceSerializer,ProductSerializer,EventImagesSerializer,
                             DeliverySerializer)

from tagging.models import TaggedItem
from tagging.models import Tag
from collections import namedtuple
from django.db.models import Q
Item = namedtuple('Item', ('product', 'service','event','delivery'))

# Create your views here.


class Explore(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,location):
        item = Item(product = models.Product.objects.filter(Q(location__icontains = location)),
                        service = models.Service.objects.filter(Q(location__icontains = location)),
                        event = models.Event.objects.filter(Q(location__icontains = location)),
                        delivery = models.Delivery.objects.filter(Q(location__icontains = location)))
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
            output_data.extend(serializer.data)
        except:
            pass
        try:
            query_set = TaggedItem.objects.get_by_model(models.Service, tag)
            serializer = ServiceSerializer(query_set,many=True)
            output_data.extend(serializer.data)
        except:
            pass
        try:
            query_set = TaggedItem.objects.get_by_model(models.Event, tag)
            serializer = EventSerializer(query_set,many=True)
            output_data.extend(serializer.data)
        except:
            pass
        try:
            query_set = TaggedItem.objects.get_by_model(models.Delivery, tag)
            serializer = DeliverySerializer(query_set,many=True)
            output_data.extend(serializer.data)
        except:
            pass
        #print(output_data)
        if output_data:
            return Response(output_data, status=status.HTTP_200_OK)
        else:
            return Response('No match',status=status.HTTP_400_BAD_REQUEST)