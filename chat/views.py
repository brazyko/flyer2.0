from django.shortcuts import render
from .models import Message,ChatRoom,ChatRoomMessage
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.utils.timezone import get_current_timezone
from django.shortcuts import redirect
from django.urls import reverse
# Create your views here.
@login_required
def chatlist(request):
    chats = ChatRoom.objects.filter(participants= request.user)
    context = {
        'chats':chats,
    }
    return render(request,'chat.html',context)

class CreateDialogView(View):
    def get(self, request, user_id):
        chats = ChatRoom.objects.filter(participants=user_id and request.user)
        if chats.count() == 0:
            chat = ChatRoom.objects.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
        else:
            chat = chats.first()
        return redirect(reverse('chat:chatroom', kwargs={'id': chat.id}))

def room(request,room_name):
    username = request.GET.get('username','Anonymous')
    chat_messages = Message.objects.all().filter(room = room_name)
    context = {
        'room_name': room_name,
        'username': username,
        'chat_messages':chat_messages,
    }
    return render(request, 'room.html',context)

@login_required
def chatroom(request,id):
    chatroom = ChatRoom.objects.all().filter(id=id)[0]
    messages = ChatRoomMessage.objects.all().filter(chatroom = chatroom)
    context = {
        'chatroom':chatroom,
        'messages':messages,
    }
    return render(request,'chatroom.html',context)