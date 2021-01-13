import json
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
from django.dispatch import receiver
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
import asyncio
from .models import ChatMessage, ChatRoom
from forum.models import ChatNotification

class ChatConsumer(WebsocketConsumer):

    def new_message(self, data):
        author = self.scope['user']
        recipient = data['other_user']
        number = data['number']

        room = ChatRoom.objects.get(number=number)

        # Update chat room's latest message and its timestamp 
        room.latest_message = data['message']
        room.latest_message_date = datetime.now()
        room.save()

        message = ChatMessage.objects.create(author=author, recipient=User.objects.get(username=recipient), content=data['message'], room=room)
        
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message),
        }

        return self.send_chat_message(content)

    def message_to_json(self, message):
        # Convert timestamp to local time
        timestamp = timezone.localtime(message.timestamp)
        return {
            'author': message.author.username,
            'author_img': message.author.profile.image.url,
            'content': message.content,
            'timestamp': timestamp.strftime("%-I:%M %p | %b %d"),
            "chat_number": str(message.room.number)
        }

    commands = {
        'new_message': new_message,
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        print(f"Connected {self.room_group_name}!")

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))

