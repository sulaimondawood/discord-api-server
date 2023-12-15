from rest_framework import serializers
from .models import Room, Topic

class RoomSerializer(serializers.ModelSerializer):
  class Meta:
    model= Room
    fields = "__all__"


class CreateRoomSerialiser(serializers.Serializer):
  topic = serializers.CharField(required=True)
  name = serializers.CharField(required=True)
  description = serializers.CharField(required=False, allow_null=True)
  avatar = serializers.ImageField(required=False)
  is_new_topic = serializers.BooleanField(default=False)


 
class TopicSerializer(serializers.ModelSerializer):
  class Meta:
    model = Topic
    fields = "__all__"