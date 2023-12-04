from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

class CustomUserManager(BaseUserManager):
  def create_superuser(self, username, display_name, email, password, **extra_fields):
    extra_fields.setdefault("is_staff", True)
    extra_fields.setdefault("is_active", True)
    extra_fields.setdefault("is_superuser", True)

    if extra_fields.get("is_staff") is not True:
      raise ValueError("Superuser must have is_staff set to True")

    if extra_fields.get("is_active") is not True:
      raise ValueError("Superuser must have is_active set to True")
    
    if extra_fields.get("is_superuser") is not True:
      raise ValueError("Superuser must have is_superser set to True")

    return self.create_user(username, display_name,email, password, **extra_fields)

  def create_user(self, username, display_name, email, password, **extra_fields):
    if not email:
      raise ValueError("The given email field must be set")
    
    email = self.normalize_email(email)
    user = self.model(username = username, display_name=display_name, email=email, password= password, **extra_fields)
    user.set_password(password)
    user.save()
    return user


class CustomUser(AbstractUser):
  username  = models.CharField(max_length=150, unique=True)
  display_name = models.CharField(max_length=120)
  email = models.EmailField(unique=True)

  objects = CustomUserManager()

  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = [ "username", "display_name"]

  def __str__(self):
    return self.username
