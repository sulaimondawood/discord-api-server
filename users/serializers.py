from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model= CustomUser
    fields = ("id","email", "username", "display_name", "password")
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


class UpdateUserSerializer(serializers.Serializer):
  id = serializers.CharField(read_only=True)
  username = serializers.CharField(required=False)
  display_name = serializers.CharField(required=False)
  email = serializers.CharField(required=False, allow_blank=True)
  avatar = serializers.ImageField(required=False, allow_null=True)

  def update(self, instance, validated_data):
    instance.username = validated_data.get('username', instance.username)
    instance.display_name = validated_data.get('display_name', instance.display_name)
    instance.email = validated_data.get('email', instance.email)
    instance.avatar = validated_data.get('avatar', instance.avatar)
    instance.save()
    return instance


  
  # def get_avatar_url(self, obj):
  #   avatar = obj.avatar
  #   request = self.context.get('request')
  #   if request:
  #     return request.build_absolute_uri(avatar)


