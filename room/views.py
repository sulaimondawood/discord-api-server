from django.db.models import Q 
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.parsers import FormParser, MultiPartParser
from .models import Room,Topic, Message
from .serializers import RoomSerializer, TopicSerializer , CreateRoomSerializer, MessageSerializer, CreateMessageSerializer
from users.models import CustomUser

from django.db.models import Q

@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def list_rooms(request):
  if request.method == "GET":
    print(request.user.id)
    instance = Room.objects.all()
    query = request.query_params.get("search")

    if query:
      instance = Room.objects.filter(Q(topic__title__icontains = query) | Q(name=query))

    room = RoomSerializer(instance, many=True, context={'request': request}).data
    return Response(room, status=status.HTTP_200_OK)
    
  elif request.method == "POST":
    print(request.data)
    serializer = CreateRoomSerializer(data=request.data)
    # serializer = RoomSerializer(data=request.data)

    if serializer.is_valid():
      topic = serializer.validated_data.get("topic")
      print(serializer.validated_data.get("name"))
      print(serializer.validated_data.get("topic"))
      print(serializer.validated_data.get("description"))
      print(request.user)
      new_topic, created = Topic.objects.get_or_create(title= topic)


      instance = Room.objects.create(
        host=request.user,
        topic=new_topic,
        description=serializer.validated_data['description'],
        avatar=serializer.validated_data['avatar'],
        name=serializer.validated_data['name'],

      )
    
      return Response(data=serializer, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])
def create_room(request):
  if request.method == "POST":
    serializer = CreateRoomSerializer(data = request.data)
    print(serializer)
    print(request.data)
    if serializer.is_valid():
      topic = serializer.validated_data["topic"]
      name = serializer.validated_data["name"]
      desc = serializer.validated_data["description"]
      new_topic, created = Topic.objects.get_or_create(title = topic )
    #  this is causing an error
      avatar = serializer.validated_data['avatar']

      instance =  Room.objects.create(host=request.user, topic= new_topic, name=name, description=desc, avatar=avatar )

    #  this is causing an error
      # instance =  Room.objects.create(host=request.user, topic= new_topic, name=name, description=desc, avatar=avatar )

      return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response({"error": "Bad request from client"}, status=status.HTTP_400_BAD_REQUEST)


      
@permission_classes([IsAuthenticated])
@api_view(["GET","PUT","DELETE", "POST"])
def get_room(request, pk):
  try:
    instance = Room.objects.get(id=pk)
  except Room.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == "GET":
    # data = RoomSerializer(instance, context={"request": request}).data
    data = RoomSerializer(instance).data
    room_messages = Message.objects.filter(room__id= pk)
    room_serialized_msgs =MessageSerializer(room_messages, many=True).data
    return Response({"data":data,"room_messages": room_serialized_msgs}, status=status.HTTP_200_OK)
  
  elif request.method == "PUT":
    serializer = RoomSerializer(instance, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(data=serializer.data)
    return Response(status=status.HTTP_400_BAD_REQUEST)
  
  elif request.method == "POST":
    serializer = CreateMessageSerializer( data=request.data, context={"request" :request, "room":instance })

    print(request.data)
    if serializer.is_valid():
      instance.members.add(request.user)
      serializer.save()
      return Response(status=status.HTTP_201_CREATED, data={"message": "message succesfully sent!"})
    
    return Response( {"error": "Error occured while sending request to server"}, status=status.HTTP_400_BAD_REQUEST,)

  
  elif request.method == "DELETE":
    instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  



@api_view(["GET", "POST"])
def list_topics(request):
  instance = Topic.objects.all()
  if request.method == "GET":
    data = TopicSerializer(instance, many=True).data
    query = request.query_params.get("search")
    if query:
      instance = Topic.objects.filter(title = query)

    return Response(data, status=status.HTTP_200_OK)
  
  if request.method == "POST":
    serializer_data = TopicSerializer(data=request.data)
    if serializer_data.is_valid():
      title_check = serializer_data.validated_data.get("title")
      topic, created =  Topic.objects.get_or_create(title=title_check)
      return Response({"message": "Topic created or retrived succesfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

  

@api_view(["GET"])
def list_msgs(request):
  if request.method == "GET":
    message = Room.message_set.all()
    serializer= MessageSerializer(message, many=True).data
    return Response(serializer, status=status.HTTP_200_OK)

  return Response(status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@api_view(["DELETE", "PUT"])
def get_msg(request, pk):
  message = Message.objects.get(pk=pk)
  if request.method == "DELETE":
    message.delete()
    return Response({"message": "succesfully deleted"}, status=status.HTTP_204_NO_CONTENT)

  if request.method == "PUT":
    serializer = CreateMessageSerializer(message, data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response({"message": "Message Updated"}, status=status.HTTP_201_CREATED)

  return Response(status=status.HTTP_400_BAD_REQUEST)
   # data = Message.objects.fillter(room__id = instance.id)
    # msg_serializer = MessageSerializer(data, many=True).data