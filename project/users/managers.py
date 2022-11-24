from django.contrib.auth.hashers import make_password
from django.contrib.auth.base_user import BaseUserManager
from .helpers import EmailManager, OTPManager
# from .models import Favorite


class CustomUserManager(BaseUserManager):
    """
    Custom user model managers where email is the unique identifiers
    for authentication instead of username
    """

    def _create_user(self, email,password,**extra_fields):
        if not email:
            raise ValueError("The email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.username = email
        # We check if password has been given
        if password:
            user.is_active = False
            EmailManager.send_welcome_msg(user.email)
            user.set_password(password)
        user.save()
        return user
    def create_user(self, email, password=None, **extra_fields):

        return self._create_user(email, password, **extra_fields)
    
    
    
    def create_user_super(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        #user.username = email
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, email,password = None, **extra_fields):
        """
        Create and save a Superuser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user_super(email,password, **extra_fields)
