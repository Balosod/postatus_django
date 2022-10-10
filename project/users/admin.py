from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (User,Product,Service,Event,Delivery,
                     ProductImages,ServiceImages,EventImages)


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

# admin.site.register(Product)
# admin.site.register(Service)
# admin.site.register(Event)
# admin.site.register(Delivery)
# admin.site.register(Upload)
@admin.register(User)
class UserAdmin(UserAdmin):
    ordering = ("email",)
    list_display = (
        "id",
        "email",
        "is_active",
        "is_staff",
        "date_joined",
    )
