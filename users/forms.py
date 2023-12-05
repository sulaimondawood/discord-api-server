from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserFrom(UserCreationForm):
  class Meta:
    model = CustomUser
    fields =  ["email", "username", "display_name", "password"]


class CustomUserChangeForm(UserChangeForm):
  class Meta:
    model = CustomUser
    fields =  ["email", "username", "display_name", "password"]