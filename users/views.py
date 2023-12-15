from rest_framework.response import Response 
from rest_framework import status, exceptions
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import UserSerializer

from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.middleware import csrf

@api_view(["GET", "POST"])
def users(request):
  if request.method == "GET":
    users = CustomUser.objects.all()
    serializer = UserSerializer(users, many=True).data
    return  Response(status=status.HTTP_200_OK, data=serializer)
  
  if request.method == "POST":
    pass


@api_view(["POST"])
def register_user(request):
  if request.method == "POST":
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()
      if user:
        return Response(status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def black_list_token(request):
  try:
    refresh_token = request.data["refresh_token"]
    token = RefreshToken(refresh_token)
    token.blacklist()
  except Exception as e:
    return Response(status=status.HTTP_400_BAD_REQUEST)
  


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
        
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    } 

@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    response = Response()
    if email is None or (password is None):
      raise exceptions.AuthenticationFailed("email and password required")
    
  
   
    user = authenticate(request, email=email,password=password)
    if user is not None:
      if user.is_active:
        data = get_tokens_for_user(user)
        response.set_cookie(
        "refresh_token",
        value=data["refresh"],
        max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
        secure=True,
        httponly=True,
        samesite="None" )

        csrf.get_token(request)
        serializer = UserSerializer(instance=user).data
        response.data = {"Success" : "Login successfully","data":data, "user":serializer }

        return response
      else:
        return Response({"No active" : "This account is not active!!"},status=status.HTTP_404_NOT_FOUND)
        
    else:
      return Response({"Invalid" : "Invalid username or password!!"},status=status.HTTP_404_NOT_FOUND)