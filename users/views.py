from rest_framework.response import Response 
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import UserSerializer

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