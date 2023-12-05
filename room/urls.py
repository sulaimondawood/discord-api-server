from django.urls import path
from .views import room

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path("", room, name="rooms")
]

urlpatterns +=  static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)