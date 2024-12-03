from django.urls import path
from . import consumers

websocket_urlpatterns = [

    path("ws/chat/<chat_name>/", consumers.ChatRoomConsumer.as_asgi()),

     
]
