from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserFrom,CustomUserChangeForm

class UserAdminConfig(UserAdmin):
  add_form= CustomUserFrom
  form = CustomUserChangeForm

  ordering= ["-created"]
  list_display = ["email","username","display_name", "is_staff", "is_active"]
  list_filter = ["email", "username", "display_name"]


admin.site.register(CustomUser, UserAdminConfig)