from django.urls import path
from . import views

app_name = 'myApp'

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]
