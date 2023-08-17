from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *


# Create your views here.

class Dashboard(APIView):
    def get(self, request):
        dist={}
        if request.user.is_authenticated:
            dist["info"]=UserInformation.objects.filter(user=request.user).first()
        return render(request, "dashboard.html", dist)

class Register(APIView):
    def post(self, request):
        print(request.data)
        user_serializer = UserValidation(data=request.data)
        user_info = UserInfoValidation(data=request.data)
        if User.objects.filter(username=request.data['username']).exists():
            return Response(
                {'Message': "Username already exists!..."},
                status=status.HTTP_409_CONFLICT
            )
        if User.objects.filter(username=request.data['email']).exists():
            return Response(
                {'Message': "Email already exists!..."},
                status=status.HTTP_409_CONFLICT
            )
        if user_serializer.is_valid():
            if user_info.is_valid():
                user = user_serializer.save()
                user_info.save(user=user)
                return redirect("myApp:login")
        return Response(
            {"Message": "Invalid data!..."},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    def get(self, request):
        return render(request, "register.html")


class Login(APIView):
    def post(self, request):
        user = User.objects.filter(email=request.data['email']).first()
        if not user:
            return Response(
                {"Message": "Username doesn't exists!..."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        user = authenticate(username=user.username, password=request.data['password'])
        if user is None:
            return Response(
                {"Message": "Incorrect password!..."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        auth_login(self.request, user)
        return redirect("myApp:dashboard")

    def get(self, request):
        return render(request, "login.html")

@method_decorator(csrf_exempt, name='dispatch')
class Logout(LoginRequiredMixin, APIView):
    def get(self, *args, **kwargs):
        auth_logout(self.request)
        return redirect("myApp:dashboard")
