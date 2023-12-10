from django.db.models import Q 
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Room,Topic
from .serializers import RoomSerializer, TopicSerializer

@api_view(["GET", "POST"])
def list_rooms(request):
  if request.method == "GET":
    instance = Room.objects.all()
    room = RoomSerializer(instance, many=True).data
    return Response(room, status=status.HTTP_200_OK)
    
  
  elif request.method == "POST":
    instance = RoomSerializer(data=request.data)
    if instance.is_valid():
      instance.save()
      return Response(data=instance.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET","PUT","DELETE"])
def get_room(request, pk):
  try:
    instance = Room.objects.get(id=pk)
  except Room.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == "GET":
    data = RoomSerializer(instance).data
    return Response(data, status=status.HTTP_200_OK)
  
  elif request.method == "PUT":
    serializer = RoomSerializer(instance, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(data=serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)
  
  elif request.method == "DELETE":
    instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  



@api_view(["GET", "POST"])
def list_topics(request):
  instance = Topic.objects.all()
  if request.method == "GET":
    data = TopicSerializer(instance, many=True).data
    return Response(data, status=status.HTTP_200_OK)
  
  if request.method == "POST":
    serializer_data = TopicSerializer(data=request.data)
    if serializer_data.is_valid():
      title_check = serializer_data.validated_data.get("title")
      topic, created =  Topic.objects.get_or_create(title=title_check)
      return Response({"message": "Topic created or retrived succesfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def search_rooms(request):
  if request.method == "GET":
    rooms = Room.objects.all()
    query = request.query_params.get("query")

    if query:
      rooms = Room.objects.filter(Q(topic__title__icontains = query) | Q(name__icontains=query) | Q(description__icontains = query))

    serializer = RoomSerializer(rooms, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
  



@api_view(["POST"])
def message_list(request):
  pass