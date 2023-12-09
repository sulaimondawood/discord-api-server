from django.urls import path
from . import views

urlpatterns = [
  path('', views.users, name="users-list"),  
  path('register/', views.register_user, name="register")
]