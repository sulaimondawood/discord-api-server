from django.db import models
from users.models import CustomUser
from django.utils import timezone

class Topic(models.Model):
  title = models.CharField(max_length=200)
  updated= models.DateTimeField(auto_now=True)
  created = models.DateTimeField( default=timezone.now)

  def __str__(self):
    return self.title

class Room(models.Model):
  host = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="rooms")
  topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="topics")
  name = models.CharField(max_length=200, null=True, blank=True)
  # members = models.ManyToManyField(CustomUser, related_name="room_members", )
  description = models.TextField(blank=True, null=True)
  avatar = models.ImageField(default="default-room-avatar.png", null=True, blank=True)
  updated= models.DateTimeField(auto_now=True)
  created = models.DateTimeField( default=timezone.now)

  def __str__(self):
    return self.name
  
  @staticmethod
  def get_all_rooms(request):
    records = []
    for val in Room.objects.all().order_by('-created'):
      data = dict(
        id=val.id,
        name=val.name,
        # topic=val.topic,  
        # host = val.host,
        # members = val.members,
        description = val.description,

      )

      image_url = request.build_absolute_uri(val.avatar.url)
      data['avatar'] = image_url
      records.append(data)

      return records

  




class Message(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_messages")
  room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room_messages")
  message = models.TextField()
  updated= models.DateTimeField(auto_now=True)
  created = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return self.message[0:30]