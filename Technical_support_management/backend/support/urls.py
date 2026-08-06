from rest_framework.routers import DefaultRouter
from support.api_view import *
from django.urls import path,include

ro = DefaultRouter()



urlpatterns = [
    path("register",UserRegistrationViewset.as_view(),name="register"),
    path("login",UserLoginViewset.as_view(),name="login"),
    path("users",UserViewset.as_view(),name="users"),
]
urlpatterns += ro.urls