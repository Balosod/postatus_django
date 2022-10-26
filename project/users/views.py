import requests as http_requests
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from . import models
import base64
import uuid
from django.core.files.base import ContentFile
from .serializers import(ProductSerializer, ServiceSerializer,EventSerializer,InterestSerializer,
                         ProductServiceEventSerializer, UserSerializer,DeliverySerializer)
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from tagging.models import Tag
from tagging.models import TaggedItem
from collections import namedtuple

User = get_user_model()
Item = namedtuple('Item', ('product', 'service','event'))


class RedirectSocial(APIView):
    def get(self, request, *args, **kwargs):
        code, state = str(request.GET['code']), str(request.GET['state'])
        json_obj = {'code': code, 'state': state}
        print(json_obj)
        return Response(json_obj)


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
        return Response('something went wrong.',status=status.HTTP_400_BAD_REQUEST)

class PostDeliveryView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        data = request.data
        data['owner'] = request.user.id
        serializer = DeliverySerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response("Delivery Sent", status=status.HTTP_200_OK)
        return Response('something went wrong.',status=status.HTTP_400_BAD_REQUEST)
    
class GetDeliveryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        query_set = models.Delivery.objects.all()
        serializer = DeliverySerializer(query_set,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request):
        data = request.data
        input_tag = data["input_tag"]
        try:
            tag = Tag.objects.get(name=input_tag)
            query_set = TaggedItem.objects.get_by_model(models.Delivery, tag)
            serializer = DeliverySerializer(query_set,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response('Tags does not exist',status=status.HTTP_400_BAD_REQUEST)
    

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        item = Item(product = models.Product.objects.all(),
                        service = models.Service.objects.all(),
                        event = models.Event.objects.all())
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
        if output_data:
            return Response(output_data, status=status.HTTP_200_OK)
        else:
            return Response('No match',status=status.HTTP_400_BAD_REQUEST)
    

class InterestView(APIView):
    def get(self,request):
        query_set = models.Interest.objects.all()
        serializer = InterestSerializer(query_set,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        query_set = User.objects.filter(email = request.user.email).first()
        serializer = UserSerializer(query_set)
        return Response(serializer.data, status=status.HTTP_200_OK) 

    def delete(self, request):
        data = request.data
        interestID = data["interestID"]
        query_set = User.objects.filter(email = request.user.email)
        interest_list = query_set.values()[0]["interests"]
        if interest_list == None:
            return Response("InterestID does not exist", status=status.HTTP_400_BAD_REQUEST)
        if interestID not in interest_list:
            return Response("InterestID does not exist", status=status.HTTP_400_BAD_REQUEST)
        else:
            interest_list.remove(interestID)
            user = query_set.update(interests=interest_list)
            return Response("InterestID has been removed", status=status.HTTP_200_OK) 

    def post(self, request):
        data = request.data
        interestID = data["interestID"]
        query_set = User.objects.filter(email = request.user.email)
        interest_list = query_set.values()[0]["interests"]
        if interest_list == None:
            interest_list = []
            interest_list.append(interestID)
            user = query_set.update(interests=interest_list)
            return Response("InterestID has been added", status=status.HTTP_200_OK)
        if interestID in interest_list:
            return Response("InterestID exist", status=status.HTTP_400_BAD_REQUEST) 
        else:
            interest_list.append(interestID)
            user = query_set.update(interests=interest_list)
            return Response("InterestID has been added", status=status.HTTP_200_OK)