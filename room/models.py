from django.db import models
from users.models import CustomUser

class Topic(models.Model):
  title = models.CharField(max_length=200)
  updated= models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)

class Room(models.Model):
  host = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="rooms")
  topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="topics")
  members = models.ManyToManyField(CustomUser, related_name="room_members")
  description = models.TextField()
  avatar = models.ImageField()
  updated= models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_messages")
  room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room_messages")
  message = models.TextField()
  updated= models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)