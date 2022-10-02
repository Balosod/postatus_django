import uuid
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from .managers import CustomUserManager


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=20, unique=False, blank=True, null=True)
    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class BaseModel(models.Model):
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    price = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    tags = models.CharField(max_length=300)
    image = models.ImageField(upload_to='upload_image')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Product(BaseModel):
    what_to_sell = models.CharField(max_length=100)
    quantity = models.CharField(max_length=30)

    class Meta:
        db_table = "Product"

    def _str_(self):
        return self.what_to_sell

class Service(BaseModel):
    what_to_do = models.CharField(max_length=300)
    delivery_type = models.CharField(max_length=300)
    duration = models.CharField(max_length=100)

    class Meta:
        db_table = "Service"

    def _str_(self):
        return self.what_to_do
    
class Event(BaseModel):
    what_is_it_about = models.CharField(max_length=300)
    medium = models.CharField(max_length=300)
    date_and_time = models.CharField(max_length=100)

    class Meta:
        db_table = "Event"

    def _str_(self):
        return self.what_is_it_about

class Delivery(models.Model):
    pick_up_location = models.CharField(max_length=300)
    delivery_location = models.CharField(max_length=300)
    category = models.CharField(max_length=100)
    delivery_type = models.CharField(max_length=100)
    set_price = models.CharField(max_length=30)
    size = models.CharField(max_length=30)
    select_category = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    tags = models.CharField(max_length=300)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def _str_(self):
        return self.pick_up_location