from django.db import models
from tagging.fields import TagField
from django.conf import settings

# Create your models here.


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
    location = models.CharField(max_length=100, null = True, blank=True)
    price = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    tags = TagField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="+", on_delete=models.CASCADE)
    

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
        
class Delivery(BaseModel):
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
    size = models.CharField(max_length=30)
    select_category = models.CharField(max_length=5,choices = DELIVERY_CHOICES, default = MOTOR_CYCLE,)

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
