from hashlib import blake2b
from random import choices
from sqlite3 import Time
from django.db import models
from django.contrib.auth.models import User
from .constants import STATUS

# Create your models here.
class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS)
    class Meta:
        abstract = True

class Customer(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, blank=True, null= True)
    profile_img = models.ImageField(upload_to="customer/profile", blank=True, null= True)

    



