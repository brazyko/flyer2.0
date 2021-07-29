import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoomMessage,ChatRoom
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from web socket
    async def receive(self, text_data):
        data = json.loads(text_data)
        chat = data['chat']
        user = data['user']
        message = data['message']

        await self.save_message(chat, user, message)
        userImage = await  self.get_user_progile_iamge_url(user)
        timestamp = self.get_current_time()
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user,
                'userImage':userImage,
                'timestamp':timestamp,
            }
        )
    
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        userImage = event['userImage']
        timestamp = event['timestamp']
        

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'userImage': userImage,
            'timestamp': timestamp,
        }))

    @database_sync_to_async
    def save_message(self, chat, user, message):
        ChatRoomMessage.objects.create(messageAuthor=User.objects.filter(username = user)[0], chatroom=ChatRoom.objects.filter(id= chat)[0], message=message)

    @database_sync_to_async
    def get_user_progile_iamge_url(self,user):
        user=User.objects.filter(username = user)[0]
        profile_img_url = str(user.profile.image.url)
        return profile_img_url
    
    def get_current_time(self):
        time = timezone.localtime(timezone.now()).strftime("%H:%M")
        return str(time)