from support.models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

class UserRegistrationViewset(APIView):

    @action(detail=False,methods=["post"],url_name="register")
    def post(self,request):
        email = request.data.get("email")
        full_name = request.data.get("full_name")
        password = request.data.get("password")
        mobile = request.data.get("mobile")

        if (email and full_name and password and mobile) == False:
            return ValueError({"message":"All fields are required"},status=400)

        user = CustomUser.objects.filter(email = email).exists()
        if user:
            return Response({"message":"User already exists"}, status=404)

        user = CustomUser.objects.create_user(
            email= email,
            full_name= full_name,
            mobile = mobile,
            password=password
        )
        return Response({"message":"user register successfull"},status=201)


class UserLoginViewset(APIView):

    @action(detail=False,methods=["post"])
    def login(self,request):
        email= request.data.get("email")
        password = request.data.get("password")

        if email and password == False:
            return ValueError({"message":"email and password is require"},status=400)

        try:
            user= CustomUser.objects.get(email=email)

        except CustomUser.DoesNotExist:
            return Response({"message":"User doesn`t exists"},status=400)

        if not user.check_password(password):
            return Response({"message":"Wrong Password"},status=400)

        return Response({
            "name":user.full_name,
            "email":user.email,
            "mobile":user.mobile
        },status=200)            


class UserViewset(APIView):

    def get(self):
        users= CustomUser.objects.all()

        total_user = users.count()

        return Response({
            "total_user":total_user,
            "users":users
        },status=200)