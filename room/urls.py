from django.urls import path
from .views import list_rooms,get_room, list_topics,search_rooms



urlpatterns = [
  path("all-rooms/", list_rooms, name="rooms"),
  path('room-details/<str:pk>/',get_room, name="room" ),
  path("topics/", list_topics, name="topic-list"),
  path("rooms/", search_rooms, name="search-rooms")
]

