from django.db import models
from users.models import CustomUser
from django.utils import timezone
from cloudinary.models import CloudinaryField

class Topic(models.Model):
  title = models.CharField(max_length=200)
  updated= models.DateTimeField(auto_now=True)
  created = models.DateTimeField( default=timezone.now)

  def __str__(self):
    return self.title

class Room(models.Model):
  host = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="rooms")
  topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="topics")
  name = models.CharField(max_length=200, blank=True, default='')
  members = models.ManyToManyField(CustomUser, related_name="room_members", )
  description = models.TextField(blank=True, default='')
  avatar = CloudinaryField('image',)
  # avatar = models.ImageField(default="default-room-avatar.png", null=True, blank=True)
  updated= models.DateTimeField(auto_now=True)
  created = models.DateTimeField( default=timezone.now)

  class Meta:
    ordering= ("-created", '-updated')

  def __str__(self):
    return self.name 
  


  




class Message(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_messages")
  room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room_messages")
  message = models.TextField()
  updated= models.DateTimeField(auto_now=True)
  created = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return self.message[0:30]