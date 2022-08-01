from django.urls import path, include
from apps.authapp.api.v1.urls import *

urlpatterns = [
    path('',include("apps.authapp.api.v1.urls")),
]