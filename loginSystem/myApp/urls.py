from django.urls import path
from . import views

app_name = 'myApp'

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('create_blog/', views.CreateBlog.as_view(), name='create_blog'),
    path('blog_list/', views.ListBlogs.as_view(), name='list_blog'),
]
