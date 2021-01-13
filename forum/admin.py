from django.contrib import admin
from .models import Post, Comment, Community, Notification, ChatNotification

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Community)
admin.site.register(Notification)
admin.site.register(ChatNotification)