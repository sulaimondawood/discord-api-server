from django.db import models

# Create your models here.
class Room(models.Model):
  # host = 
  # topic =
  # members = 
  description = models.TextField()
  avatar = models.ImageField()


class Message(models.Model):
  # user =
  # room =
  message = models.TextField()