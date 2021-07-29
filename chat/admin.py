from django.contrib import admin

from .models import Message, ChatRoom, ChatRoomMessage

admin.site.register(Message)



admin.site.register(ChatRoom)
admin.site.register(ChatRoomMessage)