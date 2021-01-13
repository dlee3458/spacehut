from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView
from forum.models import ChatNotification


class HomeView(TemplateView):
    template_name = 'notifier/home.html'

def update_chat_notification(request):
    # Updates chat messages as read if user is already in the chat
    if request.is_ajax():
        latest_notification = ChatNotification.objects.all().last()
        latest_notification.read = True
        latest_notification.save()

        return HttpResponse('ok')