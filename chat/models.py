from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Message(models.Model):
    username = models.CharField(max_length=255)
    room = models.CharField(max_length=255)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)


class ChatRoom(models.Model):
    participants = models.ManyToManyField(User, verbose_name='particapants')

class ChatRoomMessage(models.Model):
    chatroom = models.ForeignKey(ChatRoom, related_name='messages',  on_delete= models.CASCADE)
    messageAuthor = models.ForeignKey(User, on_delete= models.CASCADE)
    message = models.TextField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
