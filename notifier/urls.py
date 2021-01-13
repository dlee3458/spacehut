from django.urls import path
from .views import HomeView
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='notifier-home'),
    path('12323241/', views.update_chat_notification, name='update-chat-notification')
]