from django.shortcuts import render
from .models import Message
# Create your views here.
def index(request):
    return render(request,'chat.html')

def room(request,room_name):
    username = request.GET.get('username','Anonymous')
    chat_messages = Message.objects.all().filter(room = room_name)
    context = {
        'room_name': room_name,
        'username': username,
        'chat_messages':chat_messages,
    }
    return render(request, 'room.html',context)