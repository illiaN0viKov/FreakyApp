from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from .models import *
from asgiref.sync import async_to_sync

import json

class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.chat_name = self.scope["url_route"]["kwargs"]["chat_name"]
        self.chat = get_object_or_404(ChatGroup, chat_name=self.chat_name)

        async_to_sync(self.channel_layer.group_add)(self.chat_name, self.channel_name)

        #check and add online
        if self.user not in self.chat.users_online.all():
            self.chat.users_online.add(self.user)
            self.count_online()


        self.accept()

    def disconnect (self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.chat_name, self.channel_name)

        #check and remove online
        if self.user in self.chat.users_online.all():
            self.chat.users_online.remove(self.user)
            self.count_online()

    def receive(self, text_data):
        text_data_json=json.loads(text_data)
        text = text_data_json['text']

        message = GroupMessage.objects.create(
            text = text, 
            author = self.user,
            group = self.chat
        )

        event = {
            "type":"message_handler", 
            "message_id": message.id,
        }

        async_to_sync(self.channel_layer.group_send)(self.chat_name, event)

    def message_handler(self, event):
        message_id = event["message_id"]
        message = GroupMessage.objects.get(id=message_id)
        context = {
            "message":message,
            "user": self.user,
        }
        html = render_to_string("chat/partials/chat_message_p.html", context=context)
        self.send(text_data=html)

    def count_online(self):
        online_count = self.chat.users_online.count() - 1

        event = {
            "type":'online_count_handler', 
            "online_count":online_count
        }

        async_to_sync(self.channel_layer.group_send)(self.chat_name, event)

    def online_count_handler(self, event):
        online_count = event["online_count"]
        html = render_to_string("chat/partials/online_count.html", {"online_count": online_count})
        self.send(text_data=html)