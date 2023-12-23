from rest_framework import serializers
from .models import Room, Topic, Message
from users.serializers import UserSerializer

class RoomSerializer(serializers.ModelSerializer):
  # avatar_url =serializers.SerializerMethodField()
  class Meta:
    model= Room
    fields = ('id', "host", "topic", "name", "description", 'avatar', "updated", "created")

  # def get_avatar_url(self, obj):
  #   avatar = obj.avatar

  #   if avatar:
  #     request = self.context.get('request')
  #     return request.build_absolute_uri(avatar.url)



class CreateRoomSerializer(serializers.Serializer):
  topic = serializers.CharField(required=True)
  name = serializers.CharField(required=True)
  description = serializers.CharField(required=False, allow_null=True)
  avatar = serializers.ImageField(required=False)


  



class CreateMessageSerializer(serializers.Serializer):
  message = serializers.CharField(required= True)

  def create(self, validated_data):
    user = self.context.get("request").user
    room = self.context.get('room')
    return Message.objects.create(user=user, room= room, **validated_data)


class MessageSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  user = UserSerializer()
  room = RoomSerializer()
  message = serializers.CharField(required=True)

 
class TopicSerializer(serializers.ModelSerializer):
  class Meta:
    model = Topic
    fields = "__all__"