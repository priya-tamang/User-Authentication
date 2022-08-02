from dataclasses import field
from pyexpat import model
from attr import validate
from django import conf
from rest_framework import serializers
from apps.authapp.models import(
                        Customer,
) 
from django.contrib.auth.models import User

class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_null=True)
    first_name = serializers.CharField(allow_null=True)
    last_name = serializers.CharField(allow_null=True)
    email = serializers.CharField(allow_null=True)
    password = serializers.CharField(allow_null=True)
    confirm_password = serializers.CharField(allow_null=True)
    
    class Meta:
        model = Customer
        fields = ['username','first_name','last_name','email','password','confirm_password','profile_img','phone']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Username is not avialable"
            )
        if len(value) < 5:
            raise serializers.ValidationError(
                "Username must be at least 5 characters long.."
                
            )
    
            
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email is not avialable"
            )

    def validate(self, value):
        password = value.get('password')
        confirm_password = value.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError(
                "Password didnot match"
            )
    
    def validate_empty_email(self, value):
        if value is None:
            raise serializers.ValidationError(
                "The Email field is required. Please enter a valid email address"
            )

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_null=True)
    password = serializers.CharField(allow_null=True)