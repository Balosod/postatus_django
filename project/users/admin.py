from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from .models import (User,Product,Service,Event,Delivery,
                     ProductImages,ServiceImages,EventImages,Interest)


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


@admin.register(User)
class UserAdmin(UserAdmin):
    ordering = ("email",)
    list_display = (
        "id",
        "email",
        "interests",
        "is_active",
        "is_staff",
        "date_joined",
    )


class InterestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    class Meta:
        model = Interest

admin.site.register(Interest, InterestAdmin)
admin.site.register(Delivery)