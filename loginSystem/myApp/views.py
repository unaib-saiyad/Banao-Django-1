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
from django.core.paginator import Paginator, EmptyPage

from .models import *
from .serializers import *


# Create your views here.

def get_info(request):
    info = UserInformation.objects.filter(user=request.user).first()
    return info


class Profile(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("myApp:login")
        dist = {"info": get_info(request)}
        return render(request, "profile.html", dist)


class Dashboard(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("myApp:login")
        dist = {"info": get_info(request)}
        return render(request, "dashboard.html", dist)


class Register(APIView):
    def post(self, request):
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


class CreateBlog(APIView):
    def get(self, request):
        dist = {"info": get_info(request)}
        return render(request, 'create_blog.html', dist)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = BlogSerializer(data=request.data)
            if serializer.is_valid():
                if request.data['save_as_draft'] == "true":
                    serializer.save(user=request.user, draft=True)
                    alert = {"type": "danger", "message": "Blog drafted successfully..."}
                else:
                    serializer.save(user=request.user)
                    alert = {"type": "success", "message": "Blog created successfully..."}
                dist = {"info": get_info(request), "alert": alert}
                return render(request, 'create_blog.html', dist)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return redirect('myApp:login')


class ListBlogs(APIView):
    def get(self, request):
        page_number = int(request.GET.get('page', 1))
        category = request.GET.get('category', 'all')
        draft = (True if request.GET.get("draft") == 'true' else False)
        if category != 'all':
            if draft:
                blog_posts = Blog.objects.filter(user=request.user).filter(category=category).order_by('-created_at')
            else:
                blog_posts = Blog.objects.filter(draft=draft).filter(category=category).order_by('-created_at')
        else:
            if draft:
                blog_posts = Blog.objects.filter(user=request.user).order_by('-created_at')
            else:
                blog_posts = Blog.objects.filter(draft=draft).order_by('-created_at')
        paginator = Paginator(blog_posts, 3)  # Number of items per page
        try:
            page_obj = paginator.page(page_number)
        except EmptyPage:
            return Response({'data': [], 'has_next': False})
        blog_data = [{'title': post.title, 'summary': post.summary, 'draft': post.draft, 'user': post.user.username,
                      'image': post.image.url if post.image else ""} for post in page_obj]
        return Response({'data': blog_data, 'has_next': page_obj.has_next()})
