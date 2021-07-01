from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    DialogsView,
    CreateDialogView,
    MessagesView,
    )

app_name= 'dialogs'
urlpatterns = [
    path('', login_required(DialogsView.as_view()), name='dialogs'),
	path('create/<user_id>/', login_required(CreateDialogView.as_view()), name='create_dialog'),
	path('<chat_id>/', login_required(MessagesView.as_view()), name='messages'),
]

