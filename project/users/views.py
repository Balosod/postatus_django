import requests as http_requests
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.views import APIView
from . import models
import base64
import io
import uuid
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from .serializers import ProductServiceEventSerializer
from rest_framework.permissions import IsAuthenticated
from collections import namedtuple
Item = namedtuple('Item', ('product', 'service','event'))

from django.core.files.images import ImageFile
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile

class ActivateUserEmail(CreateAPIView):
    permission_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        uid = request.data.get("uid")
        token = request.data.get("token")
        response = None

        protocol = "https://" if request.is_secure() else "http://"
        hosts = request.get_host()
        post_url = f"{protocol}{hosts}/auth/users/activation/"
        payload = dict(uid=uid, token=token)
        res = http_requests.post(post_url, data=payload)

        response = dict(detail="success") if res.status_code < 300 else res.json()
        return Response(response)

class GoodServicesView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        owner = models.User.objects.get(email =request.user.email)
        try:
            if data['what_to_sell']:
                obj = models.Product.objects.create(what_to_sell=data['what_to_sell'], quantity=data['quantity'],
                                            category=data['category'],location=data['location'],price=data['price'],
                                            description=data['description'],tags=data['tags'],owner=owner)
                images=data['image']
                for image in images:
                    str_image = image.split("b'")
                    img_name = str(uuid.uuid4())[:10] + '.png'
                    content_file = ContentFile(base64.b64decode(str_image[1]), name=img_name)
                    uploaded_image = models.ProductImages.objects.create(img = content_file,product=obj)
                return Response("Product Sent", status=status.HTTP_200_OK)
        except:
            pass
        try:
            if data['what_to_do']:
                obj = models.Service.objects.create(what_to_do=data['what_to_do'], 
                                            delivery_type=data['delivery_type'],duration=data['duration'],
                                            category=data['category'],location=data['location'],price=data['price'],
                                            description=data['description'],tags=data['tags'],owner=owner)
                images=data['image']
                for image in images:
                    str_image = image.split("b'")
                    img_name = str(uuid.uuid4())[:10] + '.png'
                    content_file = ContentFile(base64.b64decode(str_image[1]), name=img_name)
                    uploaded_image = models.ServiceImages.objects.create(img = content_file,service=obj)
                return Response("Service Sent", status=status.HTTP_200_OK)
        except:
            pass
        try:
            if data['what_is_it_about']:
                obj = models.Event.objects.create(what_is_it_about=data['what_is_it_about'], 
                                            medium=data['medium'],date_and_time=data['date_and_time'],
                                            category=data['category'],location=data['location'],price=data['price'],
                                            description=data['description'],tags=data['tags'],owner=owner)
                images=data['image']
                for image in images:
                    str_image = image.split("b'")
                    img_name = str(uuid.uuid4())[:10] + '.png'
                    content_file = ContentFile(base64.b64decode(str_image[1]), name=img_name)
                    uploaded_image = models.EventImages.objects.create(img = content_file,event=obj)
                return Response("Event Sent", status=status.HTTP_200_OK)
        except:
            pass
        return Response('something went wrong',status=status.HTTP_400_BAD_REQUEST)

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        item = Item(product = models.Product.objects.all(),
                        service = models.Service.objects.all(),
                        event = models.Event.objects.all())
        serializer = ProductServiceEventSerializer(item)
        
        return Response(serializer.data, status=status.HTTP_200_OK) 
            