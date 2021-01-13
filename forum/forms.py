from django import forms
from .models import Comment, Post, Community
from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'comment-control form-control', 'placeholder': 'Add a comment...', 'rows':'1', 'cols':'50'}))

    class Meta:
        model = Comment
        fields = ('content',)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('community', 'title', 'content', 'image',)

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content',)

class CommunityForm(forms.ModelForm):

    class Meta:
        model = Community
        fields = ('name', 'about', 'thumbnail',)

        


       
