from django.urls import path
from django.contrib.auth.decorators import login_required
from users.views import (
    show_all_users, 
    show_user_profile,
    )

app_name= 'users'
urlpatterns = [
    path('',show_all_users, name='user-list'),
    path('<user_slug>',show_user_profile, name='user-profile'),
]

