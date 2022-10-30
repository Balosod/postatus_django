from django.contrib import admin
from .models import (Product,Service,Event,Delivery,
                     ProductImages,ServiceImages,EventImages)

# Register your models here.
# Setting up admin panel for Product
class ProductImagesAdmin(admin.StackedInline):
    model = ProductImages

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
 
    class Meta:
       model = Product

# @admin.register(ProductImages)
# class ProductImagesAdmin(admin.ModelAdmin):
#     pass

# Setting up admin panel for Service
class ServiceImagesAdmin(admin.StackedInline):
    model = ServiceImages

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    inlines = [ServiceImagesAdmin]
 
    class Meta:
       model = Service

# @admin.register(ServiceImages)
# class ServiceImagesAdmin(admin.ModelAdmin):
#     pass


# Setting up admin panel for Event
class EventImagesAdmin(admin.StackedInline):
    model = EventImages

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [EventImagesAdmin]
 
    class Meta:
       model = Event

# @admin.register(EventImages)
# class EventImagesAdmin(admin.ModelAdmin):
#     pass

admin.site.register(Delivery)