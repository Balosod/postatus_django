from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    ordering = ("email",)
    list_display = (
        "id",
        "email",
        "image",
        "interests",
        "is_active",
        "is_staff",
        "date_joined",
    )