from django.contrib import admin
from .models import Interest

# Register your models here.

class InterestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    class Meta:
        model = Interest

admin.site.register(Interest, InterestAdmin)

