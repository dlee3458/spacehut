from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from json import dumps
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.loader import render_to_string
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from .models import ChatRoom, ChatMessage
from forum.models import ChatNotification

def index(request):
    chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-latest_message_date')

    # Create two-dimensional list [[chat_room, notification_count], ..] for easier filtering
    user_chat_rooms = []
    for user_chat_room in chat_rooms:
        count = ChatNotification.objects.filter(recipient=request.user, chat_room=user_chat_room, read=False).count()
        user_chat_rooms.append([user_chat_room, count])

    context =  {
        'user_chat_rooms': user_chat_rooms
    }

    if request.is_ajax():
        html = render_to_string('chat/index.html', context, request=request)
        return JsonResponse({'chat_index': html})
    
    return render(request, 'chat/index.html', context)

def room(request, room_name):
    chat_id = int(room_name)
    recipient_id = chat_id - request.user.id
    recipient = User.objects.get(id=recipient_id)
    
    # Verify if the current room is an existing chat room
    if ChatRoom.objects.filter(number=chat_id).exists():
        exisiting_room = ChatRoom.objects.get(number=chat_id)
        saved_messages = ChatMessage.objects.filter(room=exisiting_room).order_by('timestamp')

        # Set any unread messages as read when user visits chat room
        ChatNotification.objects.filter(recipient=request.user, chat_room=exisiting_room).update(read=True)

        content = {
            'room_name': room_name,
            'user': request.user,
            'other_user': recipient,
            'messages': saved_messages,
        }
    
    # Create a new chat room if current room does not exist
    else:
        new_room = ChatRoom.objects.create(
            name=request.user.username + '/' + recipient.username,
            number=chat_id,
            sender=request.user,
            receiver=recipient)
        new_room.users.add(request.user)
        new_room.users.add(recipient)

        content = {
            'room_name': room_name,
            'user': request.user,
            'other_user': recipient,
            'user_chat_room': new_room,
            'chat_room_id': str(chat_id),
        }
        
        if request.is_ajax():
            new_chat_room = render_to_string('chat/prepend_new_chat_room.html', content, request=request)
            html = render_to_string('chat/room_popup_ajax.html', content, request=request)
            return JsonResponse({'form': html, 'new_chat_room': new_chat_room})
   
    # Filter out the chat rooms that the current user is a part of
    chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-latest_message_date')
    content['chat_room_id'] = str(chat_id)

    # Create two-dimensional list [[chat_room, notification_count], ..] for easier filtering
    user_chat_rooms = []
    for user_chat_room in chat_rooms:
        count = ChatNotification.objects.filter(recipient=request.user, chat_room=user_chat_room, read=False).count()
        user_chat_rooms.append([user_chat_room, count])

    content['user_chat_rooms'] = user_chat_rooms

    if request.is_ajax():
        html = render_to_string('chat/room_popup_ajax.html', content, request=request)
        return JsonResponse({'form': html})
    
    return render(request, 'chat/room.html', content)

def prepend_new_chat(request, room_name):
    chat_id = int(room_name)
    chat_room = ChatRoom.objects.get(number=chat_id)

    context = {
        'user_chat_room': chat_room
    }

    new_chat_room = render_to_string('chat/prepend_new_chat_room.html', context, request=request)
    return JsonResponse({'new_chat_room': new_chat_room})

def start_new_chat(request):
    if request.is_ajax():
        users_followings = request.user.profile.followings.all()
        ajax_context = {
            'followings': users_followings,
        }

        html = render_to_string('chat/start_new_chat.html', ajax_context, request=request)
        return JsonResponse({'form': html})

def find_user(request, input):
    if request.is_ajax():
        print(input)
        matched_users = User.objects.filter(username__icontains=input)

        ajax_context = {
            'matched_users': matched_users
        }

        html = render_to_string('chat/matched_users.html', ajax_context, request=request)
        return JsonResponse({'matched_users': html})
