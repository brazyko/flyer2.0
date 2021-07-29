from django.urls import path
from django.contrib.auth.decorators import login_required
from chat.views import chatlist,room,chatroom,CreateDialogView

app_name= 'chat'
urlpatterns = [
    path('',chatlist,name='chatlist'),
    path('create/<user_id>/', login_required(CreateDialogView.as_view()), name='create_chatroom'),
    path('<id>/',chatroom,name='chatroom'),
]