from distutils import extension
from operator import is_

from yaml import serialize
from apps.authapp.models import (
                                    Customer
)
from apps.authapp.api.v1.serializers import (
                                            CustomerSerializer,
                                            UserLoginSerializer
)
from rest_framework.views import APIView, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.parsers import FormParser, MultiPartParser
from apps.authapp.utils import get_token_for_user


class CustomerRegisterAPIView(APIView):
    parser_classes = (FormParser, MultiPartParser)
    @extend_schema(request=CustomerSerializer)
    def post(self,request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        # print("serializers :", serializers)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            phone = serializer.validated_data.get('phone')

            user = User.objects.create_user(username=username,email=email,first_name=first_name,last_name=last_name, password=password)
            # print("user :", user)
            customer = Customer.objects.create(status="Active",user=user,phone=phone)
            resp = {
                "status": "success",
                "message": "Account successfully created"
            }

        else:
            resp = {
                "status": "failure",
                "message": serializer.errors
            }
        return Response(resp)

class CustomerLoginAPIView(APIView):
    @extend_schema(request=UserLoginSerializer)
    def post(self,request):
        serializers = UserLoginSerializer(data=request.data) 
        if serializers.is_valid(raise_exception=True):
            email = serializers.validated_data.get("email")
            password = serializers.validated_data.get("password")
            try:
                customer_obj = Customer.objects.get(user__email=email)
                user = customer_obj.user.check_password(password)
                if not user:
                    resp = {
                        "message": "Your email or password is incorrect."
                    }
                    return Response(resp, status=status.HTTP_401_UNAUTHORIZED)
                if customer_obj.status == "Active" and customer_obj.user.is_active:
                    resp = get_token_for_user(customer_obj.user)
                    return Response(resp)
                else:
                    resp = {
                        "message": "Pending or Suspended account. Please contact your administrator"
                    }
                    return Response(resp, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e: # kun exception auncha thacha vane tei catch gara la
                resp = {
                    "message": str(e)
                }
        else:
            resp = {
                "message": "Missing Information, please try again"
            }
        return Response(resp, status=status.HTTP_401_UNAUTHORIZED)

    

