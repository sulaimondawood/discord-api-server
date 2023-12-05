from rest_framework import serializers
from .models import Room, Topic

class RoomSerializer(serializers.ModelSerializer):
  class Meta:
    model= Room
 
class TopicSerializer(serializers.ModelSerializer):
  class Meta:
    model = Topic
    fields = "__all__"