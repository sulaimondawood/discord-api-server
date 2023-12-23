from django.urls import path
from .views import list_rooms,get_room, list_topics,search_rooms,create_room, list_msgs, get_msg



urlpatterns = [
  path("all-rooms/", list_rooms, name="rooms"),
  path('room-server/<str:pk>/',get_room, name="room" ),
  path("topics/", list_topics, name="topic-list"),
  path("search-rooms/", search_rooms, name="search-rooms"),
  path('create-room/', create_room, name='create-room' ),
  path('delete-edit-msg/<int:pk>', get_msg, name='room-message' ),
  # path('room-messages/',list_msgs )
]

