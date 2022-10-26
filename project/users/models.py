import uuid
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from .managers import CustomUserManager
from tagging.fields import TagField



class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=20,unique=False, blank=True, null=True)
    email = models.EmailField(unique=True)
    interests = ArrayField(models.IntegerField(),null = True, blank= True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Interest(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class BaseModel(models.Model):
    FOOD_AND_DRINKS = "FD"
    GRAPHIC_DESIGN = "GD"
    RECREATIONAL_AND_FUN_FAIR = 'RFF'
    
    CATEGORY_CHOICES = [
        (FOOD_AND_DRINKS, "FOOD AND DRINKS"),
        (GRAPHIC_DESIGN, "GRAPHIC DESIGN"),
        (RECREATIONAL_AND_FUN_FAIR,"RECREATIONAL AND FUN FAIR"),
    ]
    
    category = models.CharField(max_length=5,choices = CATEGORY_CHOICES, default = FOOD_AND_DRINKS,)
    location = models.CharField(max_length=100)
    price = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    tags = TagField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    

    class Meta:
        abstract = True

class Product(BaseModel):
    what_to_sell = models.CharField(max_length=100)
    quantity = models.CharField(max_length=30)

    class Meta:
        db_table = "Product"

    def __str__(self):
        return self.owner.email

class Service(BaseModel):
    ONLINE = "ON"
    OFFLINE = "OFF"
    
    DELIVERY_CHOICES = [
        (ONLINE, "ONLINE"),
        (OFFLINE, "OFFLINE"),
    ]
    what_to_do = models.CharField(max_length=300)
    delivery_type = models.CharField(max_length=5,choices = DELIVERY_CHOICES, default = OFFLINE,)
    duration = models.CharField(max_length=100)

    class Meta:
        db_table = "Service"

    def __str__(self):
        return self.owner.email
    
class Event(BaseModel):
    ONLINE = "ON"
    OFFLINE = "OFF"
    
    MEDIUM_CHOICES = [
        (ONLINE, "ONLINE"),
        (OFFLINE, "OFFLINE"),
    ]
    what_is_it_about = models.CharField(max_length=300)
    medium = models.CharField(max_length=5,choices = MEDIUM_CHOICES, default = OFFLINE,)
    date_and_time = models.CharField(max_length=100)

    class Meta:
        db_table = "Event"

    def __str__(self):
        return self.owner.email
        
class Delivery(models.Model):
    INTER_STATE = "IS"
    WITHIN_STATE = "WS"
    
    CATEGORY_CHOICES = [
        (INTER_STATE, "INTER_STATE"),
        (WITHIN_STATE, "WITHIN_STATE"),
    ]
    
    MOTOR_CYCLE = "MC"
    MINI_VAN = "MV"
    TRUCK = "TR"
    
    DELIVERY_CHOICES = [
        (MOTOR_CYCLE, "MOTOR_CYCLE"),
        (MINI_VAN, "MINI_VAN"),
        (TRUCK, "TRUCK"),
    ]
    pick_up_location = models.CharField(max_length=300)
    delivery_location = models.CharField(max_length=300)
    category = models.CharField(max_length=5,choices = CATEGORY_CHOICES, default = INTER_STATE,)
    delivery_type = models.CharField(max_length=5,choices = DELIVERY_CHOICES, default = MOTOR_CYCLE,)
    set_price = models.CharField(max_length=30)
    size = models.CharField(max_length=30)
    select_category = models.CharField(max_length=5,choices = DELIVERY_CHOICES, default = MOTOR_CYCLE,)
    description = models.CharField(max_length=300)
    tags = TagField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.owner.email


class ProductImages(models.Model):
    img = models.ImageField()
    product = models.ForeignKey(Product,related_name="posts", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.img}"

class ServiceImages(models.Model):
    img = models.ImageField()
    service = models.ForeignKey(Service, related_name="posts", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.img}"

class EventImages(models.Model):
    img = models.ImageField()
    event = models.ForeignKey(Event, related_name="posts", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.img}"
