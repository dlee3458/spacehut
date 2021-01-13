from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from forum.models import Notification, Comment, Post, ChatNotification
from chat.models import ChatMessage

@receiver(post_save, sender=Comment)
def create_comment_notiication(sender, instance, created, **kwargs):
    if created:
        if instance.reply_parent:
            Notification.objects.create(
                post=instance.post,
                comment=instance,
                sender=instance.user,
                recipient=instance.reply_parent.user,
                reply_notification=True
            )

            user_room_name = str(instance.reply_parent.user.id)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                user_room_name, {
                    "type": "user_notification",
                    "event": "New notification",
                    "post": instance.post.title,
                    "notification_count": Notification.objects.filter(recipient=instance.reply_parent.user, read=False).count()
                }
            )
        
        elif instance.parent:
            Notification.objects.create(
                post=instance.post,
                comment=instance,
                sender=instance.user,
                recipient=instance.parent.user,
                reply_notification=True
            )

            user_room_name = str(instance.parent.user.id)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                user_room_name, {
                    "type": "user_notification",
                    "event": "New notification",
                    "post": instance.post.title,
                    "notification_count": Notification.objects.filter(recipient=instance.parent.user, read=False).count()
                }
            )
       
        else:
            Notification.objects.create(
                post=instance.post,
                comment=instance,
                sender=instance.user,
                recipient=instance.post.author,
                comment_notification=True
            )

            user_room_name = str(instance.post.author.id)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                user_room_name, {
                    "type": "user_notification",
                    "event": "New notification",
                    "post": instance.post.title,
                    "notification_count": Notification.objects.filter(recipient=instance.post.author, read=False).count()
                }
            )

@receiver(m2m_changed, sender=Post.likes.through)
def create_likepost_notification(sender, instance, action, **kwargs):
    if action == 'post_add':
        Notification.objects.create(
            post=instance,
            sender=instance.likes.through.objects.last().user,
            recipient=instance.author,
            like_post_notification=True
        )

        user_room_name = str(instance.author.id)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            user_room_name, {
                "type": "user_notification",
                "event": "New notification",
                "notification_count": Notification.objects.filter(recipient=instance.author, read=False).count()
            }
        )
        
    
@receiver(m2m_changed, sender=Comment.likes.through)
def create_likecomment_notification(sender, instance, action, **kwargs):
    if action == 'post_add':
        Notification.objects.create(
            post=instance.post,
            sender=instance.likes.through.objects.last().user,
            recipient=instance.user,
            like_comment_notification=True,
            comment=instance
        )

        user_room_name = str(instance.user.id)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            user_room_name, {
                "type": "user_notification",
                "event": "New notification",
                "notification_count": Notification.objects.filter(recipient=instance.user, read=False).count()
            }
        )

@receiver(post_save, sender=ChatMessage)
def create_message_notification(sender, instance, created, **kwargs):
    if created:
        ChatNotification.objects.create(
            sender=instance.author,
            recipient=instance.recipient,
            message=instance.content,
            chat_room=instance.room
        )

        user_room_room = str(instance.recipient.id)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            user_room_room, {
                "type": "chat_notification",
                "event": "New chat",
                "chat_number": str(instance.room.number),
                "chat_notification_count": ChatNotification.objects.filter(recipient=instance.recipient, read=False).count(),
                "content": instance.content,
                "sender_img": instance.author.profile.image.url,
                "sender": instance.author.username,
                "latest_timestamp": instance.timestamp.strftime("%b %d")
            }
        )
