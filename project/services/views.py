from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from . import models
import base64
import uuid
from django.core.files.base import ContentFile
from .serializers import(ProductSerializer, ServiceSerializer,EventSerializer,DeliverySerializer)
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class GoodServices(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        try:
            if data['what_to_sell']:
                data['owner'] = request.user.id
                serializer = ProductSerializer(data=data)
                if serializer.is_valid():
                    obj = serializer.save()
                images=data['image']
                for image in images:
                    #str_image = image.split("b'")
                    img_name = str(uuid.uuid4())[:10] + '.png'
                    content_file = ContentFile(base64.b64decode(image), name=img_name)
                    print(content_file)
                    uploaded_image = models.ProductImages.objects.create(img = content_file,product=obj)
                return Response("Product Sent", status=status.HTTP_200_OK)
        except:
            pass
        try:
            if data['what_to_do']:
                data['owner'] = request.user.id
                serializer = ServiceSerializer(data=data)
                if serializer.is_valid():
                    obj = serializer.save()
                images=data['image']
                for image in images:
                    #str_image = image.split("b'")
                    img_name = str(uuid.uuid4())[:10] + '.png'
                    content_file = ContentFile(base64.b64decode(image), name=img_name)
                    uploaded_image = models.ServiceImages.objects.create(img = content_file,service=obj)
                return Response("Service Sent", status=status.HTTP_200_OK)
        except:
            pass
        try:
            if data['what_is_it_about']:
                data['owner'] = request.user.id
                serializer = EventSerializer(data=data)
                if serializer.is_valid():
                    obj = serializer.save()
                images=data['image']
                for image in images:
                    #str_image = image.split("b'")
                    img_name = str(uuid.uuid4())[:10] + '.png'
                    content_file = ContentFile(base64.b64decode(image), name=img_name)
                    uploaded_image = models.EventImages.objects.create(img = content_file,event=obj)
                return Response("Event Sent", status=status.HTTP_200_OK)
        except:
            pass
        try:
            if data['pick_up_location']:
                print('yes1')
                data['owner'] = request.user.id
                serializer = DeliverySerializer(data = data)
                print('yes2')
                if serializer.is_valid():
                    print('yes3')
                    serializer.save()
                    print('yes4')
                    return Response("Delivery Sent", status=status.HTTP_200_OK)
        except:
            pass
        return Response('something went wrong.',status=status.HTTP_400_BAD_REQUEST)