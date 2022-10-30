from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from project.services import models
from project.services.serializers import (ProductSerializer,ServiceSerializer,EventSerializer,
                                         DeliverySerializer)
# Create your views here.

class ExploreDetail(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        data = request.data
        title = data['title']
        ID = data['id']
        try:
           query_set = models.Product.objects.filter(what_to_sell=title).get(id=ID)
           serializer = ProductSerializer(query_set)
           return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            pass
        try:
           query_set = models.Service.objects.filter(what_to_do=title).get(id=ID)
           serializer = ServiceSerializer(query_set)
           return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            pass
        try:
           query_set = models.Event.objects.filter(what_is_it_about=title).get(id=ID)
           serializer = EventSerializer(query_set)
           return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            pass
        try:
           query_set = models.Delivery.objects.filter(pick_up_location=title).get(id=ID)
           serializer = DeliverySerializer(query_set)
           return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            pass
        return Response('something went wrong.',status=status.HTTP_400_BAD_REQUEST)