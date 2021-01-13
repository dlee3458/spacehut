from django.db import models
from django.contrib.auth.models import User 

class ChatRoom(models.Model):
    name = models.TextField()
    users = models.ManyToManyField(User, related_name='chat_users')
    number = models.IntegerField()
    sender = models.ForeignKey(User, related_name='chat_starter', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='chat_receiver', on_delete=models.CASCADE)
    latest_message = models.TextField(blank=True, null=True)
    latest_message_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

class ChatMessage(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='recipient_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(ChatRoom, related_name='message', on_delete=models.CASCADE)

    def __str__(self):
        return self.author.username

        