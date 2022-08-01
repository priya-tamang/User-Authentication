from distutils import extension
from operator import is_
from apps.authapp.models import (
                                    Customer
)
from apps.authapp.api.v1.serializers import (
                                            CustomerSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.parsers import FormParser, MultiPartParser


class CustomerRegisterAPIView(APIView):
    parser_classes = (FormParser, MultiPartParser)
    @extend_schema(request=CustomerSerializer)
    def post(self,request):
        serializers = CustomerSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            username = serializers.validated_data.get('username')
            email = serializers.validated_data.get('email')
            password = serializers.validated_data.get('password')
            first_name = serializers.validated_data.get('first_name')
            last_name = serializers.validated_data.get('last_name')
            phone = serializers.validated_data.get('phone')
            user = User.objects.create_user(username=username,email=email,first_name=first_name,last_name=last_name)
            customer = Customer.objects.create(status="Active",user=user,phone=phone)
            resp = {
                "status": "success",
                "message": "Account successfully created"
            }
            return Response(resp)

        else:
            resp = {
                "status": "failure",
                "message": serializers.errors
            }
            return Response(resp)

