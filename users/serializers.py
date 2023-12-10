from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model= CustomUser
    fields = ("email", "username", "display_name", "password")
    extra_kwargs = {"password":{"write_only":True}}


  def create(self, validated_data):
    user= CustomUser.objects.create(email=validated_data["email"], username=validated_data["username"], display_name=validated_data["display_name"])
    user.set_password(validated_data["password"])
    user.save()
    return user
  
    
    
  def update(self, instance, validated_data):
    password = validated_data.pop("password", None)
    user = super().update(instance, validated_data),
    if password:
      user.set_password(password)
      user.save()
    return user
