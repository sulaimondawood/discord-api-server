from django.urls import path
from . import views

urlpatterns = [
  path('', views.users, name="users-list"),  
  path('<int:pk>/', views.get_user, name="users-list"),  
  path('?search/', views.users, name="users-list"),  
  path('register/', views.register_user, name="register"),
  path('login/', views.login, name="login")
]