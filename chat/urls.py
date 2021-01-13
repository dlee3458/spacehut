from django.urls import path, re_path

from . import views

urlpatterns = [
    path('<str:room_name>/', views.room, name='room'),
    path('chats/index/', views.index, name='chat-index'),
    path('prepend_new_chat/<str:room_name>/', views.prepend_new_chat, name='prepend-new-chat'),
    path('new/start_chat/', views.start_new_chat, name='start-new-chat'),
    path('search_user/<str:input>/', views.find_user, name='find-user'),
]