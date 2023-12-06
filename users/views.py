from rest_framework.response import Response 
from rest_framework import status
from rest_framework.decorators import api_view
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
