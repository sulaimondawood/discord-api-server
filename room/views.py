from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Room,Topic
from .serializers import RoomSerializer, TopicSerializer

@api_view(["GET"])
def list_rooms(request):
  instance = Room.objects.all()
  room = RoomSerializer(instance, many=True).data
  return Response(room, status=status.HTTP_200_OK)


@api_view(["GET","PUT","DELETE", "POST"])
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
  
  elif request.method == "POST":
    instance = RoomSerializer(data=request.data)
    if instance.is_valid():
      instance.save()
      return Response(data=instance.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def list_topics(request):
  instance = Topic.objects.all()
  if request.method == "GET":
    data = TopicSerializer(instance, many=True).data
    return Response(data, status=status.HTTP_200_OK)
  
  if request.method == "POST":
    serializer_data = TopicSerializer(data=request.data)
    if data.is_valid():
      serializer_data.save()
      return Response(data= serializer_data.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

