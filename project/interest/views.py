from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from . import models
from .serializers import InterestSerializer

# Create your views here.


class Interest(APIView):
    def get(self,request):
        query_set = models.Interest.objects.all()
        serializer = InterestSerializer(query_set,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 