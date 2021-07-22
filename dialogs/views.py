from django.shortcuts import render
from django.views.generic import View
from .models import Chat,Message,VoiceMessage
from .forms import MessageForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.forms.models import model_to_dict
import json
from django.http import HttpResponse
# Create your views here.
class DialogsView(View):
    def get(self, request):
        chats = Chat.objects.filter(members=request.user)
        if request.is_ajax():
            response_data = {}
            chats = Chat.objects.filter(members=request.user)
            for c in chats:
                response_record = {}
                response_record['id'] = c.id
                response_data.update(response_record)
            return JsonResponse(response_data,safe=False,status=200)     
        context = {
            'chats': chats
            }
        return render(request, 'dialogs.html',context )

class CreateDialogView(View):
    def get(self, request, user_id):
        chats = Chat.objects.filter(members=user_id and request.user)
        if chats.count() == 0:
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
        else:
            chat = chats.first()
        return redirect(reverse('dialogs:messages', kwargs={'chat_id': chat.id}))


class MessagesView(View):
    def get(self, request, chat_id):
        chat = Chat.objects.get(id=chat_id)
        msgs ={}
        if request.is_ajax():
            messages = Message.objects.all().exclude(author = request.user).filter(is_readed = False).order_by('-pub_date')
            if messages.count() == 0:
                return JsonResponse('nmsg',safe=False,status=200)
            response_data = {}
            for m in messages:
                response_record = {}
                response_record['chat'] = m.chat.id
                response_record['author'] = m.author.username
                response_record['image_url'] = m.author.profile.image.url
                response_record['message'] = m.message
                response_record['is_readed'] = m.is_readed
                response_record['pub_date'] = m.pub_date
                response_data.update(response_record)
                m.is_readed = True
                m.save()
            return JsonResponse(response_data,safe=False,status=200)
        try:
            if request.user in chat.members.all():
                chat.message_set.filter(is_readed=False).exclude(author = request.user).update(is_readed = True)
                msgs=chat.message_set.all().order_by('pub_date')
            else:
                chat = None 
        except Chat.DoesNotExist:
            chat = None
        
        return render(
            request,
            'messages.html',
            context={
                'user_profile': request.user,
                'chat': chat,
                'msgs':msgs,
                'form': MessageForm()
            }
        )
 
    def post(self, request, chat_id):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            author = message.author
            message.save()
            return JsonResponse({'message': model_to_dict(message),'author':model_to_dict(author)},status=200)
        else:
            redirect('dialogs')

 