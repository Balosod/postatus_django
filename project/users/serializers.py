from rest_framework import serializers
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "image",
            "interests",
        )
        read_only_fields = ("username",)


# class CreateUserSerializer(serializers.ModelSerializer):
#     def create(self, validated_data):
#         # call create_user on user object. Without this
#         # the password will be stored in plain text.
#         user = User.objects.create_user(**validated_data)
#         return user

#     class Meta:
#         model = User
#         fields = (
#             "id",
#             "username",
#             "password",
#             "first_name",
#             "last_name",
#             "email",
#             "auth_token",
#         )
#         read_only_fields = ("auth_token",)
#         extra_kwargs = {"password": {"write_only": True}}


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta:
        model = User
        fields = ('id', 'email','password','interests','image',)
    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")
        return user
    
    
class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    
class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
