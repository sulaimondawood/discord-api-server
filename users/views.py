from rest_framework.response import Response 
from rest_framework import status, exceptions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import UserSerializer, UpdateUserSerializer

from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.middleware import csrf
from django.db.models import Q


@api_view(["GET", "POST"])
def users(request):
  if request.method == "GET":
    users = CustomUser.objects.all()

    query = request.query_params.get("search")
    print(query)
    if query:
      users = CustomUser.objects.filter(Q(username__icontains = query ))
    serializer = UpdateUserSerializer(users, many=True, context={'request':request}).data
    return  Response(status=status.HTTP_200_OK, data=serializer)
  

@permission_classes([IsAuthenticated])
@api_view(["GET", "PUT"])
def get_user(request, pk):
  try:
    user = CustomUser.objects.filter(id=pk)
  except user.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  
  if request.method == "GET":
    serializer = UpdateUserSerializer(user, many=True, context={'request':request})
    return Response(serializer.data ,status=status.HTTP_200_OK)


  if request.method == "PUT":
    user = CustomUser.objects.get(id=pk)
    serializer = UpdateUserSerializer(user, data=request.data, context={'request':request})
    if serializer.is_valid():
      serializer.save()
      return Response({"message":"User succesfully updated!"}, status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_400)
    



@api_view(["POST"])
def register_user(request):
  if request.method == "POST":
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()

      if not user.avatar or user.avatar is None:
        default_avatar = 'https://res.cloudinary.com/dgvamsrn5/image/upload/v1704163332/default-avatar_qldtaf.png'
        user.avatar = default_avatar
        user.save()

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
        domain="https://dawood-discord.vercel.app",
        samesite="None" )

        csrf.get_token(request)
        serializer = UserSerializer(instance=user).data
        response.data = {"Success" : "Login successfully","data":data, "user":serializer }

        return response
      else:
        return Response({"No active" : "This account is not active!!"},status=status.HTTP_404_NOT_FOUND)
        
    else:
      return Response({"Invalid" : "Invalid email or password!!"},status=status.HTTP_400_BAD_REQUEST)