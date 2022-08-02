from django.urls import path
from apps.authapp.api.v1.api import *

urlpatterns = [
    path('customer/register',CustomerRegisterAPIView.as_view(),name='customerregister'),
    path('customer/login',CustomerLoginAPIView.as_view(),name='customerlogin'),
]