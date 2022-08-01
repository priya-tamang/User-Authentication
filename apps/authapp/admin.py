from django.contrib import admin

from apps.authapp.models import (
                                    Customer,
)

# Register your models here.
@admin.register(Customer)
class registerAdmin(admin.ModelAdmin):
    list_display = ['user','phone']
