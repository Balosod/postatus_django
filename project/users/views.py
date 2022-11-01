import requests as http_requests
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from . import models
from . import auth_service
import base64
import uuid
from django.core.files.base import ContentFile
from .serializers import UserSerializer,OTPSerializer,EmailSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model




User = get_user_model()



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
    
class VerifyOtp(APIView):
    def post(self,request):
        data = request.data
        serializer = OTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = auth_service.verify_OTP(**serializer.validated_data)
        return Response(status=status.HTTP_200_OK, data=obj)

class ResendOtp(APIView):
    def post(self,request):
        data = request.data
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = auth_service.resend_OTP(**serializer.validated_data)
        return Response(status=status.HTTP_200_OK, data=obj)

class UserProfile(APIView):
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
        try:
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
        except:
            pass
        try:
            image = data['image']
            img_name = str(uuid.uuid4())[:10] + '.png'
            content_file = ContentFile(base64.b64decode(image), name=img_name)
            query_set = User.objects.get(email = request.user.email)
            query_set.image = content_file
            query_set.save()
            return Response("Image Successfully uploaded", status=status.HTTP_200_OK)
        except:
            return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST) 