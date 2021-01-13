from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User 
from django.db.models import Count
from PIL import Image
from chat.models import ChatRoom

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, related_name='likes', blank=True, on_delete=models.CASCADE)
    dislikes = models.ManyToManyField(User, related_name="forum_posts", blank=True)
    likes = models.ManyToManyField(User, related_name="f_posts", blank=True)
    saves = models.ManyToManyField(User, related_name='saved_by', blank=True)
    image = models.ImageField(upload_to='post_images', blank=True)
    community = models.ForeignKey('Community', on_delete=models.CASCADE, related_name='post_group')
    trending_points = models.IntegerField(default=0)

    class Meta:
        ordering = ['-trending_points']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('forum-home')

    # def save(self, *args, **kwargs):
    #     super(Post, self).save(*args, **kwargs)

    #     if self.image:
    #         img = Image.open(self.image.path)

    #         if img.height > 300 or img.width > 300:
    #             basewidth = 600
    #             wpercent = (basewidth/float(img.size[0]))
    #             hsize = int((float(img.size[1])*float(wpercent)))
    #             img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    #             img.save(self.image.path)
    #     else:
    #         pass

        

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    dislikes = models.ManyToManyField(User, related_name="comment_dislike", blank=True)
    likes = models.ManyToManyField(User, related_name="comment_like", blank=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    reply_parent = models.ForeignKey('self', null=True, blank=True, related_name='reply_parents', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} -{}'.format(self.post.title, str(self.user.username))

class Community(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User, related_name="group", blank=True)
    members_count = models.IntegerField(default=0)
    thumbnail = models.ImageField(default='community_thumbnails/rocket (1).png', upload_to="community_thumbnails", blank=True)
    creator = models.ForeignKey(User, related_name="community", blank=True, on_delete=models.CASCADE)
    about = models.TextField()

    class Meta:
        ordering = ['-members_count']

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     super(Community, self).save(*args, **kwargs)

    #     img = Image.open(self.thumbnail.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.thumbnail.path)
    #     else: 
    #         pass

    def get_absolute_url(self):
        return reverse('forum-home')

class Notification(models.Model):
    post = models.ForeignKey(Post, blank=True, null=True, related_name='notification', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, blank=True, null=True, related_name='comment_notification', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    sender = models.ForeignKey(User, related_name='notification_sender' ,on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='notification_recipient' ,on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    like_post_notification = models.BooleanField(default=False)
    like_comment_notification = models.BooleanField(default=False)
    comment_notification = models.BooleanField(default=False)
    reply_notification = models.BooleanField(default=False)

class ChatNotification(models.Model):
    sender = models.ForeignKey(User, related_name='message_sender', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='message_receiver', on_delete=models.CASCADE)
    message = models.TextField()
    chat_room = models.ForeignKey(ChatRoom, related_name='chat_alerts', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    
