from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, reverse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F
from django.db.models import Count
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib import messages
from .models import Post, Comment, Community, Notification
from .forms import CommentForm, PostForm, CommunityForm, PostUpdateForm
from chat.models import ChatRoom, ChatMessage
from .models import ChatNotification

def home(request):
    context = {}
    posts = Post.objects.all().order_by('-date_posted')

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context['posts'] = posts
    context['section'] = 'Home'
    context['section_img'] = '/media/house.svg'
    context['title'] = 'SpaceHut'

    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipient=request.user, read=False).count()
        chat_notifications = ChatNotification.objects.filter(recipient=request.user, read=False).count()
        context['notifications'] = notifications
        context['chat_notifications'] = chat_notifications
        
        communities = Community.objects.filter(members=request.user).order_by('name')
        context['personal_communities'] = communities
        
        chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-latest_message_date')
        user_chat_rooms = []
        for user_chat_room in chat_rooms:
            count = ChatNotification.objects.filter(recipient=request.user, chat_room=user_chat_room, read=False).count()
            user_chat_rooms.append([user_chat_room, count])

        context['user_chat_rooms'] = user_chat_rooms
    
    if request.is_ajax():
        if request.method == "POST":
            ajax_context = {
                'posts': posts,
            }

            html = render_to_string('forum/home_posts_ajax.html', ajax_context, request=request)
            side_html = render_to_string('forum/main_community_list.html', ajax_context, request=request)
            return JsonResponse({'form': html, 'communities': side_html})

    return render(request, 'forum/home.html', context)

def home_top_posts(request):
    context = {}
    posts = Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context['posts'] = posts
    context['section'] = 'Home'
    context['section_img'] = '/media/house.svg'
    context['title'] = 'SpaceHut'

    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipient=request.user, read=False).count()
        chat_notifications = ChatNotification.objects.filter(recipient=request.user, read=False).count()
        context['notifications'] = notifications
        context['chat_notifications'] = chat_notifications

        communities = Community.objects.filter(members=request.user).order_by('name')
        context['personal_communities'] = communities

        chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-latest_message_date')
        user_chat_rooms = []
        for user_chat_room in chat_rooms:
            count = ChatNotification.objects.filter(recipient=request.user, chat_room=user_chat_room, read=False).count()
            user_chat_rooms.append([user_chat_room, count])

        context['user_chat_rooms'] = user_chat_rooms

    if request.is_ajax():
        if request.method == "POST":
            ajax_context = {
                'posts': posts,
            }

            html = render_to_string('forum/home_posts_ajax.html', ajax_context, request=request)
            return JsonResponse({'form': html})

    return render(request, 'forum/home_top_posts.html', context)

def home_trending_posts(request):
    context = {}
    all_posts = Post.objects.all()
    for post in all_posts:
        total_points = post.likes.count() + post.dislikes.count() + post.post.count()
        post.trending_points = F('trending_points') + total_points
        post.save()

    posts = Post.objects.order_by('-trending_points')

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context['posts'] = posts
    context['section'] = 'Home'
    context['section_img'] = '/media/house.svg'
    context['title'] = 'SpaceHut'

    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipient=request.user, read=False).count()
        chat_notifications = ChatNotification.objects.filter(recipient=request.user, read=False).count()
        context['notifications'] = notifications
        context['chat_notifications'] = chat_notifications

        communities = Community.objects.filter(members=request.user).order_by('name')
        context['personal_communities'] = communities

        chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-latest_message_date')
        user_chat_rooms = []
        for user_chat_room in chat_rooms:
            count = ChatNotification.objects.filter(recipient=request.user, chat_room=user_chat_room, read=False).count()
            user_chat_rooms.append([user_chat_room, count])

        context['user_chat_rooms'] = user_chat_rooms

    if request.is_ajax():
        if request.method == "POST":
            ajax_context = {
                'posts': posts,
            }

            html = render_to_string('forum/home_posts_ajax.html', ajax_context, request=request)
            return JsonResponse({'form': html})

    return render(request, 'forum/home_trending_posts.html', context)

def community_detail_new(request, name):
    context = {}
    community = get_object_or_404(Community, name=name)
    posts = Post.objects.filter(community=community.id).order_by('-date_posted')
    
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    if request.user.is_authenticated:
        chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-latest_message_date')
        user_chat_rooms = []
        for user_chat_room in chat_rooms:
            count = ChatNotification.objects.filter(recipient=request.user, chat_room=user_chat_room, read=False).count()
            user_chat_rooms.append([user_chat_room, count])

        notifications = Notification.objects.filter(recipient=request.user, read=False).count()
        chat_notifications = ChatNotification.objects.filter(recipient=request.user, read=False).count()

        communities = Community.objects.filter(members=request.user).order_by('name')
        context['personal_communities'] = communities

        context['notifications'] = notifications
        context['chat_notifications'] = chat_notifications
        context['user_chat_rooms'] = user_chat_rooms

    context['posts'] = posts
    context['community'] = community
    context['section'] = community.name
    context['section_img'] = community.thumbnail.url
    context['title'] = community.name

    if request.is_ajax():
        if request.method == 'POST':
            ajax_context = context
            html = render_to_string('forum/community_ajax.html', ajax_context, request=request)
            side_html = render_to_string('forum/about_community.html', ajax_context, request=request)
            community_list = render_to_string('forum/main_community_list.html', request=request)
            top_html = render_to_string('forum/community_header.html', request=request)
            return JsonResponse({'form': html, 'about': side_html, 'header': top_html, 'communities': community_list})

    return render(request, 'forum/community.html', context)

def community_detail_trending(request, name):
    context = {}
    community = get_object_or_404(Community, name=name)
    all_posts = Post.objects.filter(community=community.id)
    for post in all_posts:
        total_points = post.likes.count() + post.dislikes.count() + post.post.count()
        post.trending_points = F('trending_points') + total_points
        post.save()

    posts = all_posts.order_by('-trending_points')

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-latest_message_date')
        user_chat_rooms = []
        for user_chat_room in chat_rooms:
            count = ChatNotification.objects.filter(recipient=request.user, chat_room=user_chat_room, read=False).count()
            user_chat_rooms.append([user_chat_room, count])

        notifications = Notification.objects.filter(recipient=request.user, read=False).count()
        chat_notifications = ChatNotification.objects.filter(recipient=request.user, read=False).count()

        communities = Community.objects.filter(members=request.user).order_by('name')
        context['personal_communities'] = communities

        context['notifications'] = notifications
        context['chat_notifications'] = chat_notifications
        context['user_chat_rooms'] = user_chat_rooms

    context['posts'] = posts
    context['community'] = community
    context['section'] = community.name
    context['section_img'] = community.thumbnail.url
    context['title'] = community.name

    if request.is_ajax():
        if request.method == 'POST':
            ajax_context = context
            html = render_to_string('forum/community_ajax.html', ajax_context, request=request)
            return JsonResponse({'form': html})

    return render(request, 'forum/community_trending_posts.html', context)

def community_list(request):
    context = {}
    communities = Community.objects.all()

    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipient=request.user, read=False).count()
        chat_notifications = ChatNotification.objects.filter(recipient=request.user, read=False).count()

        chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-latest_message_date')
        user_chat_rooms = []
        for user_chat_room in chat_rooms:
            count = ChatNotification.objects.filter(recipient=request.user, chat_room=user_chat_room, read=False).count()
            user_chat_rooms.append([user_chat_room, count])

        personal_communities = Community.objects.filter(members=request.user).order_by('name')
        context['personal_communities'] = personal_communities

        context['notifications'] = notifications
        context['chat_notifications'] = chat_notifications
        context['user_chat_rooms'] = user_chat_rooms
    
    context['communities'] = communities
    context['section'] = 'Communities'
    context['section_img'] = '/media/community.svg'
    context['title'] = 'Communities'

    if request.is_ajax():
        
        ajax_context = {
            'communities': communities,
        }

        html = render_to_string('forum/communities_all_ajax.html', ajax_context, request=request)
        side_html = render_to_string('forum/main_community_list.html', request=request)
        return JsonResponse({'form': html, 'communities': side_html})
    
    return render(request, 'forum/communities_all.html', context)
    


def community_detail_top(request, name):
    context = {}
    community = get_object_or_404(Community, name=name)
    all_posts = Post.objects.filter(community=community.id)
    
    posts = all_posts.annotate(num_likes=Count('likes')).order_by('-num_likes')

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-latest_message_date')
        user_chat_rooms = []
        for user_chat_room in chat_rooms:
            count = ChatNotification.objects.filter(recipient=request.user, chat_room=user_chat_room, read=False).count()
            user_chat_rooms.append([user_chat_room, count])

        notifications = Notification.objects.filter(recipient=request.user, read=False).count()
        chat_notifications = ChatNotification.objects.filter(recipient=request.user, read=False).count()

        communities = Community.objects.filter(members=request.user).order_by('name')
        context['personal_communities'] = communities

        context['notifications'] = notifications
        context['chat_notifications'] = chat_notifications
        context['user_chat_rooms'] = user_chat_rooms

    context['posts'] = posts
    context['community'] = community
    context['section'] = community.name
    context['section_img'] = community.thumbnail.url
    context['title'] = community.name

    if request.is_ajax():
        if request.method == 'POST':
            ajax_context = context
            html = render_to_string('forum/community_ajax.html', ajax_context, request=request)
            return JsonResponse({'form': html})

    return render(request, 'forum/community_top_posts.html', context)

@login_required
def create_post_home(request):
    if request.is_ajax():
        if request.method == 'POST':
            post_form = PostForm(request.POST, request.FILES or None)
        
            if post_form.is_valid():
                new_post = post_form.save(commit=False)
                new_post.author = request.user
                new_post.save()
                
                posts = Post.objects.all().order_by('-date_posted')

                page = request.GET.get('page', 1)
                paginator = Paginator(posts, 10)
                
                try:
                    posts = paginator.page(page)
                except PageNotAnInteger:
                    posts = paginator.page(1)
                except EmptyPage:
                    posts = paginator.page(paginator.num_pages)

                ajax_context = {
                    'posts': posts
                }
                
                # If form is valid, return JsonResponse to redirect to home page
                html = render_to_string('forum/home_posts_ajax.html', ajax_context, request=request)
                return JsonResponse({'form': html})
        else:
            post_form = PostForm()
            ajax_context = {
                'form': post_form,
            }

            side_html = render_to_string('forum/main_community_list.html', request=request)
            html = render_to_string('forum/post_form_ajax.html', ajax_context, request=request)
            return JsonResponse({'form': html, 'communities': side_html})

    else:
        chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-latest_message_date')
        user_chat_rooms = []
        for user_chat_room in chat_rooms:
            count = ChatNotification.objects.filter(recipient=request.user, chat_room=user_chat_room, read=False).count()
            user_chat_rooms.append([user_chat_room, count])

        communities = Community.objects.filter(members=request.user).order_by('name')
        post_form = PostForm()

        context = {
            'form': post_form,
            'section': 'Create Post',
            'section_img': '/media/writing.svg',
            'personal_communities': communities,
            'user_chat_rooms': user_chat_rooms,
            'title': 'Create Post'
        }
        return render(request, 'forum/post_form.html', context)

@login_required
def create_community_post(request, name):
    community = get_object_or_404(Community, name=name)
    if request.is_ajax():

        if request.method == 'GET':
            post_form = PostForm(initial={'community': community})
            ajax_context = {
                'form': post_form,
            }

            html = render_to_string('forum/post_form_ajax.html', ajax_context, request=request)
            side_html = render_to_string('forum/main_community_list.html', request=request)
            return JsonResponse({'form': html, 'communities': side_html})

    else:
        post_form = PostForm(initial={'community': community})
        notifications = Notification.objects.filter(recipient=request.user, read=False).count()
        chat_notifications = ChatNotification.objects.filter(recipient=request.user, read=False).count()

        chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-latest_message_date')
        user_chat_rooms = []
        for user_chat_room in chat_rooms:
            count = ChatNotification.objects.filter(recipient=request.user, chat_room=user_chat_room, read=False).count()
            user_chat_rooms.append([user_chat_room, count])

        communities = Community.objects.filter(members=request.user).order_by('name')

        context = {
            'form': post_form,
            'user_chat_rooms': user_chat_rooms,
            'notifications': notifications,
            'chat_notifications': chat_notifications,
            'personal_communities': communities,
            'section': 'Create Post',
            'section_img': '/media/writing.svg',
            'title': 'Create Post',
        }
        return render(request, 'forum/post_form.html', context)


@login_required
def create_community(request):
    if request.is_ajax():
        if request.method == 'POST':
            community_form = CommunityForm(request.POST, request.FILES or None)
        
            if community_form.is_valid():
                new_community = community_form.save(commit=False)
                new_community.creator = request.user
                new_community.save()

                ajax_context = {
                    'community': new_community,
                }
                
                # If form is valid, ajaxify new community page
                html = render_to_string('forum/community_ajax.html', ajax_context, request=request)
                side_html = render_to_string('forum/about_community.html', ajax_context, request=request)
                community_list = render_to_string('forum/main_community_list.html', request=request)
                top_html = render_to_string('forum/community_header.html', request=request)
                return JsonResponse({'form': html, 'about': side_html, 'header': top_html, 'communities': community_list})
        else:
            community_form = CommunityForm()
            ajax_context = {
                'form': community_form,
            }

            html = render_to_string('forum/community_form_ajax.html', ajax_context, request=request)
            side_html = render_to_string('forum/main_community_list.html', request=request)
            return JsonResponse({'form': html, 'communities': side_html})

    else:
        community_form = CommunityForm()
        notifications = Notification.objects.filter(recipient=request.user, read=False).count()
        chat_notifications = ChatNotification.objects.filter(recipient=request.user, read=False).count()
        
        chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-latest_message_date')
        user_chat_rooms = []
        for user_chat_room in chat_rooms:
            count = ChatNotification.objects.filter(recipient=request.user, chat_room=user_chat_room, read=False).count()
            user_chat_rooms.append([user_chat_room, count])

        communities = Community.objects.filter(members=request.user).order_by('name')
        
        context = {
            'form': community_form,
            'notifications': notifications,
            'chat_notifications': chat_notifications,
            'user_chat_rooms': user_chat_rooms,
            'section': 'Create Community',
            'section_img': '/media/people.svg',
            'personal_communities': communities,
            'title': 'Create new community'
        }
        return render(request, 'forum/community_form.html', context)

def user_posts(request, username):
    context = {}
    user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(author=user).order_by('-date_posted')

    page = request.GET.get('page', 1)
    paginator = Paginator(user_posts, 10)
    
    try:
        user_posts = paginator.page(page)
    except PageNotAnInteger:
        user_posts = paginator.page(1)
    except EmptyPage:
        user_posts = paginator.page(paginator.num_pages)

    post_likes = 0
    post_dislikes = 0
    comment_likes = 0 
    comment_dislikes = 0
    user_comments = Comment.objects.filter(user=user)
    communities = Community.objects.filter(members=user)
    
    for post in user_posts:
        post_likes += post.likes.count()
        post_dislikes += post.dislikes.count()
    
    for comment in user_comments:
        comment_likes += comment.likes.count()
        comment_dislikes += comment.dislikes.count()

    total_post_points = post_likes - post_dislikes
    total_comment_points = comment_likes - comment_dislikes
    
    space_points = total_post_points + total_comment_points

    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipient=request.user, read=False).count()
        chat_notifications = ChatNotification.objects.filter(recipient=request.user, read=False).count()
        
        chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-latest_message_date')
        user_chat_rooms = []
        for user_chat_room in chat_rooms:
            count = ChatNotification.objects.filter(recipient=request.user, chat_room=user_chat_room, read=False).count()
            user_chat_rooms.append([user_chat_room, count])

        # Determine whether user is following this profile or not
        if request.user.profile.followings.filter(id=user.id).exists():
            is_following = True
        else:
            is_following = False

        personal_communities = Community.objects.filter(members=request.user).order_by('name')
        context['personal_communities'] = personal_communities

        context['notifications'] = notifications
        context['chat_notifications'] = chat_notifications
        context['user_chat_rooms'] = user_chat_rooms
        context['chat_id'] = request.user.id + user.id
        context['is_following'] = is_following

    context['communities'] = communities
    context['user'] = user
    context['space_points'] = space_points
    context['posts'] = user_posts
    context['section'] = user.username
    context['section_img'] = user.profile.image.url
    context['title'] = user.username + "'s Profile"

    if request.is_ajax():
        if request.method == 'POST':
            ajax_context = context
            
            html = render_to_string('forum/user_posts_ajax.html', ajax_context, request=request)
            user_info = render_to_string('forum/user_info.html', ajax_context, request=request)
            return JsonResponse({'form': html, 'user_info': user_info})

    return render(request, 'forum/user_posts.html', context)

def user_posts_trending(request, username):
    context = {}
    user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(author=user)
    for post in user_posts:
        total_points = post.likes.count() + post.dislikes.count() + post.post.count()
        post.trending_points = F('trending_points') + total_points
        post.save()

    posts = user_posts.order_by('-trending_points')

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    post_likes = 0
    post_dislikes = 0
    comment_likes = 0 
    comment_dislikes = 0
    user_comments = Comment.objects.filter(user=user)
    user_posts = Post.objects.filter(author=user)
    communities = Community.objects.filter(members=user)
    
    for post in user_posts:
        post_likes += post.likes.count()
        post_dislikes += post.dislikes.count()
    
    for comment in user_comments:
        comment_likes += comment.likes.count()
        comment_dislikes += comment.dislikes.count()

    total_post_points = post_likes - post_dislikes
    total_comment_points = comment_likes - comment_dislikes
    
    space_points = total_post_points + total_comment_points

    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipient=request.user, read=False).count()
        chat_notifications = ChatNotification.objects.filter(recipient=request.user, read=False).count()
        
        chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-latest_message_date')
        user_chat_rooms = []
        for user_chat_room in chat_rooms:
            count = ChatNotification.objects.filter(recipient=request.user, chat_room=user_chat_room, read=False).count()
            user_chat_rooms.append([user_chat_room, count])

        # Determine whether user is following this profile or not
        if request.user.profile.followings.filter(id=user.id).exists():
            is_following = True
        else:
            is_following = False

        personal_communities = Community.objects.filter(members=request.user).order_by('name')
        context['personal_communities'] = personal_communities

        context['notifications'] = notifications
        context['chat_notifications'] = chat_notifications
        context['user_chat_rooms'] = user_chat_rooms
        context['chat_id'] = request.user.id + user.id
        context['is_following'] = is_following

    context['communities'] = communities
    context['user'] = user
    context['space_points'] = space_points
    context['posts'] = user_posts
    context['section'] = user.username
    context['section_img'] = user.profile.image.url
    context['title'] = user.username + "'s Profile"

    if request.is_ajax():
        if request.method == 'POST':
            ajax_context = context
            html = render_to_string('forum/user_posts_ajax.html', ajax_context, request=request)
            user_info = render_to_string('forum/user_info.html', ajax_context, request=request)
            return JsonResponse({'form': html, 'user_info': user_info})

    return render(request, 'forum/user_posts_trending.html', context)

def user_posts_top(request, username):
    context = {}
    user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(author=user)
    
    posts = user_posts.annotate(num_likes=Count('likes')).order_by('-num_likes')

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    post_likes = 0
    post_dislikes = 0
    comment_likes = 0 
    comment_dislikes = 0
    user_comments = Comment.objects.filter(user=user)
    user_posts = Post.objects.filter(author=user)
    communities = Community.objects.filter(members=user)
    
    for post in user_posts:
        post_likes += post.likes.count()
        post_dislikes += post.dislikes.count()
    
    for comment in user_comments:
        comment_likes += comment.likes.count()
        comment_dislikes += comment.dislikes.count()

    total_post_points = post_likes - post_dislikes
    total_comment_points = comment_likes - comment_dislikes
    
    space_points = total_post_points + total_comment_points

    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipient=request.user, read=False).count()
        chat_notifications = ChatNotification.objects.filter(recipient=request.user, read=False).count()
        
        chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-latest_message_date')
        user_chat_rooms = []
        for user_chat_room in chat_rooms:
            count = ChatNotification.objects.filter(recipient=request.user, chat_room=user_chat_room, read=False).count()
            user_chat_rooms.append([user_chat_room, count])

        # Determine whether user is following this profile or not
        if request.user.profile.followings.filter(id=user.id).exists():
            is_following = True
        else:
            is_following = False

        personal_communities = Community.objects.filter(members=request.user).order_by('name')
        context['personal_communities'] = personal_communities

        context['notifications'] = notifications
        context['chat_notifications'] = chat_notifications
        context['user_chat_rooms'] = user_chat_rooms
        context['chat_id'] = request.user.id + user.id
        context['is_following'] = is_following

    context['communities'] = communities
    context['user'] = user
    context['space_points'] = space_points
    context['posts'] = user_posts
    context['section'] = user.username
    context['section_img'] = user.profile.image.url
    context['title'] = user.username + "'s Profile"

    if request.is_ajax():
        if request.method == 'POST':
            ajax_context = context
            html = render_to_string('forum/user_posts_ajax.html', ajax_context, request=request)
            user_info = render_to_string('forum/user_info.html', ajax_context, request=request)
            return JsonResponse({'form': html, 'user_info': user_info})

    return render(request, 'forum/user_posts_top.html', context)

def user_notifications(request, username):
    user = get_object_or_404(User, username=username)

    chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-latest_message_date')
    user_chat_rooms = []
    for user_chat_room in chat_rooms:
        count = ChatNotification.objects.filter(recipient=request.user, chat_room=user_chat_room, read=False).count()
        user_chat_rooms.append([user_chat_room, count])

    chat_notifications = ChatNotification.objects.filter(recipient=request.user, read=False).count()

    communities = Community.objects.filter(members=request.user).order_by('name')

    if request.user == user:
        user_notifications_list = Notification.objects.filter(recipient=user).order_by('-date')

        Notification.objects.filter(recipient=user).update(read=True)


        context = {
            'user_notifications_list': user_notifications_list,
            'user_chat_rooms': user_chat_rooms,
            'chat_notifications': chat_notifications,
            'personal_communities': communities,
            'section': 'Notifications',
            'section_img': '/media/bell (1).svg',
            'title': 'Notifications',
        }

        if request.is_ajax():
            ajax_context = context
            
            html = render_to_string('forum/notifications_ajax.html', ajax_context, request=request)
            side_html = render_to_string('forum/main_community_list.html', request=request)
            return JsonResponse({'form': html, 'communities': side_html})

        return render(request, 'forum/notifications.html', context)
    else:
        return render(request, 'forum/access_denied.html')

@login_required
def saved(request):
    saved_posts = Post.objects.filter(saves=request.user)

    chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-latest_message_date')
    user_chat_rooms = []
    for user_chat_room in chat_rooms:
        count = ChatNotification.objects.filter(recipient=request.user, chat_room=user_chat_room, read=False).count()
        user_chat_rooms.append([user_chat_room, count])

    notifications = Notification.objects.filter(recipient=request.user, read=False).count()
    chat_notifications = ChatNotification.objects.filter(recipient=request.user, read=False).count()

    communities = Community.objects.filter(members=request.user).order_by('name')

    context = {
        'saved_posts': saved_posts,
        'notifications': notifications,
        'chat_notifications': chat_notifications,
        'user_chat_rooms': user_chat_rooms,
        'section': 'Saved',
        'section_img': "/media/floppy-disk.svg",
        'personal_communities': communities,
        'title': 'Saved Posts'
    }

    if request.is_ajax():
        ajax_context = context
        html = render_to_string('forum/saved_posts_ajax.html', ajax_context, request=request)
        side_html = render_to_string('forum/main_community_list.html', ajax_context, request=request)

        return JsonResponse({'form': html, 'communities': side_html})
    
    return render(request, 'forum/saved_posts.html', context)
    
def post_detail(request, id):
    context = {}
    post = get_object_or_404(Post, id=id)
    comments = Comment.objects.filter(post=post, active=True, parent__isnull=True).order_by('-id')

    if request.user.is_authenticated:
        chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-latest_message_date')
        user_chat_rooms = []
        for user_chat_room in chat_rooms:
            count = ChatNotification.objects.filter(recipient=request.user, chat_room=user_chat_room, read=False).count()
            user_chat_rooms.append([user_chat_room, count])

        notifications = Notification.objects.filter(recipient=request.user, read=False).count()
        chat_notifications = ChatNotification.objects.filter(recipient=request.user, read=False).count()

        communities = Community.objects.filter(members=request.user).order_by('name')
        context['personal_communities'] = communities

        context['notifications'] = notifications
        context['chat_notifications'] = chat_notifications
        context['user_chat_rooms'] = user_chat_rooms

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            parent_obj = None
            proceed = True
            
            try:
                reply_parent_id = int(request.POST.get('reply_parent_id'))
                parent_id = int(request.POST.get('parent_id'))
            except:
                reply_parent_id = None
                parent_id= None
            
            if reply_parent_id and parent_id:
                reply_parent_obj = Comment.objects.get(id=reply_parent_id)
                parent_obj = Comment.objects.get(id=parent_id)
                reply_to_reply = comment_form.save(commit=False)
                reply_to_reply.parent = parent_obj
                reply_to_reply.reply_parent = reply_parent_obj
                new_reply = comment_form.save(commit=False)
                new_reply.user = request.user
                new_reply.post = post
                new_reply.save()
                proceed = False

            if proceed:
                try:
                    parent_id = int(request.POST.get('parent_id'))
                except:
                    parent_id= None
                
                if parent_id:
                    parent_obj = Comment.objects.get(id=parent_id)
                    if parent_obj:
                        reply_comment = comment_form.save(commit=False)
                        reply_comment.parent = parent_obj

                new_comment = comment_form.save(commit=False)
                new_comment.user = request.user
                new_comment.post = post
                new_comment.save()

    else:
        comment_form = CommentForm()

    context['post'] = post
    context['comments'] = comments
    context['comment_form'] = comment_form
    context['section'] = post.community.name
    context['section_img'] = post.community.thumbnail.url
    context['title'] = post.title

    if request.is_ajax():
        if request.method == "GET":
            html = render_to_string('forum/post_detail_ajax.html', context, request=request)
            side_html = render_to_string('forum/main_community_list.html', context, request=request)
            return JsonResponse({'form': html, 'communities': side_html})
        else:
            html = render_to_string('forum/comments.html', context, request=request)
            return JsonResponse({'form': html})

    return render(request, 'forum/post_detail.html', context)

def post_comment_notification(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    main_comment = Comment.objects.get(id=comment_id)

    chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-latest_message_date')
    user_chat_rooms = []
    for user_chat_room in chat_rooms:
        count = ChatNotification.objects.filter(recipient=request.user, chat_room=user_chat_room, read=False).count()
        user_chat_rooms.append([user_chat_room, count])

    notifications = Notification.objects.filter(recipient=request.user, read=False).count()
    chat_notifications = ChatNotification.objects.filter(recipient=request.user, read=False).count()
    communities = Community.objects.filter(members=request.user).order_by('name')

    if main_comment.parent:
        comments = Comment.objects.filter(id=main_comment.parent.id, post=post, active=True).order_by('-id')
    else:
        comments = Comment.objects.filter(id=comment_id ,post=post, active=True).order_by('-id')
    
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            parent_obj = None
            proceed = True
            
            try:
                reply_parent_id = int(request.POST.get('reply_parent_id'))
                parent_id = int(request.POST.get('parent_id'))
            except:
                reply_parent_id = None
                parent_id= None
            
            if reply_parent_id and parent_id:
                reply_parent_obj = Comment.objects.get(id=reply_parent_id)
                parent_obj = Comment.objects.get(id=parent_id)
                reply_to_reply = comment_form.save(commit=False)
                reply_to_reply.parent = parent_obj
                reply_to_reply.reply_parent = reply_parent_obj
                new_reply = comment_form.save(commit=False)
                new_reply.user = request.user
                new_reply.post = post
                new_reply.save()
                proceed = False

            if proceed:
                try:
                    parent_id = int(request.POST.get('parent_id'))
                except:
                    parent_id= None
                
                if parent_id:
                    parent_obj = Comment.objects.get(id=parent_id)
                    if parent_obj:
                        reply_comment = comment_form.save(commit=False)
                        reply_comment.parent = parent_obj

                new_comment = comment_form.save(commit=False)
                new_comment.user = request.user
                new_comment.post = post
                new_comment.save()
    
            # return HttpResponseRedirect(reverse('post-detail', kwargs={'id':post_id}))

    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'main_comment': main_comment,
        'comments': comments,
        'comment_form': comment_form,
        'notifications': notifications,
        'chat_notifications': chat_notifications,
        'user_chat_rooms': user_chat_rooms,
        'personal_communities': communities,
        'section': post.community,
        'section_img': post.community.thumbnail.url,
    }

    if request.is_ajax():
        if request.method == 'GET':
            ajax_context = context

            html = render_to_string('forum/post_comment_notification_ajax.html', ajax_context, request=request)
            return JsonResponse({'form': html})
        else:
            html = render_to_string('forum/comment_replies.html', context, request=request)
            return JsonResponse({'form': html})

    return render(request, 'forum/post_comment_notification.html', context)

@login_required
def update_post(request, pk):
    original_post = Post.objects.get(id=pk)
    notifications = Notification.objects.filter(recipient=request.user, read=False).count()
    chat_notifications = ChatNotification.objects.filter(recipient=request.user, read=False).count()
    communities = Community.objects.filter(members=request.user).order_by('name')

    chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-latest_message_date')
    user_chat_rooms = []
    for user_chat_room in chat_rooms:
        count = ChatNotification.objects.filter(recipient=request.user, chat_room=user_chat_room, read=False).count()
        user_chat_rooms.append([user_chat_room, count])
    
    context = {
        'notifications': notifications,
        'chat_notifications': chat_notifications,
        'user_chat_rooms': user_chat_rooms,
        'post': original_post,
        'personal_communities': communities,
        'section': 'Update Post',
        'section_img': '/media/edit.svg',
        'title': 'Update Post'
    }

    if request.is_ajax():
        if request.method == 'POST':
            post_update_form = PostUpdateForm(request.POST, instance=original_post)
            comments = Comment.objects.filter(post=original_post, active=True, parent__isnull=True).order_by('-id')
            comment_form = CommentForm()
        
            if post_update_form.is_valid():
                updated_post = post_update_form.save(commit=False)
                updated_post.save()
                messages.success(request, f'Post updated successfully')

                ajax_context = {
                    'post': original_post,
                    'comments': comments,
                    'comment_form': comment_form,
                }
                
                html = render_to_string('forum/post_detail_ajax.html', ajax_context, request=request)
                return JsonResponse({'form': html})
        else:
            post_update_form = PostUpdateForm(instance=original_post)
            context['form'] = post_update_form

            ajax_context = context

            html = render_to_string('forum/update_post_ajax.html', ajax_context, request=request)
            return JsonResponse({'form': html})

    else:
        post_update_form = PostUpdateForm(instance=original_post)
        context['form'] = post_update_form 

        return render(request, 'forum/update_post.html', context)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post 
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True 
        return False

    def get_context_data(self, **kwargs):
        context = super(PostDeleteView, self).get_context_data(**kwargs)
        
        notifications = Notification.objects.filter(recipient=self.request.user, read=False).count()
        context['notifications'] = notifications
        return context

@login_required
def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    notifications = Notification.objects.filter(recipient=request.user, read=False).count()
    chat_notifications = ChatNotification.objects.filter(recipient=request.user, read=False).count()
    communities = Community.objects.filter(members=request.user).order_by('name')

    chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-latest_message_date')
    user_chat_rooms = []
    for user_chat_room in chat_rooms:
        count = ChatNotification.objects.filter(recipient=request.user, chat_room=user_chat_room, read=False).count()
        user_chat_rooms.append([user_chat_room, count])

    context = {
        'notifications': notifications,
        'chat_notifications': chat_notifications,
        'user_chat_rooms': user_chat_rooms,
        'post': post,
        'personal_communities': communities
    }

    if request.is_ajax():
        if request.method == 'POST':
            post.delete()
            messages.success(request, f'Post deleted successfully')

            ajax_context = context
            posts = Post.objects.all().order_by('-date_posted')

            page = request.GET.get('page', 1)
            paginator = Paginator(posts, 10)
            
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)

            ajax_context['posts'] = posts

            html = render_to_string('forum/home_posts_ajax.html', ajax_context, request=request)
            side_html = render_to_string('forum/main_community_list.html', request=request)
            return JsonResponse({'form': html, 'communities': side_html})

        else:
            html = render_to_string('forum/delete_post_ajax.html', context, request=request)
            return JsonResponse({'form': html})
    
    else:
        return render(request, 'forum/delete_post.html', context)
        

def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))
    
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True

    if is_liked and post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)

    context = {
        'post': post,
        'is_liked': is_liked,
    }
    
    if request.is_ajax():
        html = render_to_string('forum/like_section.html', context, request=request)
        return JsonResponse({'form': html})

def dislike_post(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))


    is_disliked = False
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
        is_disliked = False
    else:
        post.dislikes.add(request.user)
        is_disliked = True

    if is_disliked and post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    
    context = {
        'post': post,
        'is_disliked': is_disliked
    }

    if request.is_ajax():
        html = render_to_string('forum/like_section.html', context, request=request)
        return JsonResponse({'form': html})

def like_comment(request):
    comment = get_object_or_404(Comment, id=request.POST.get('id'))
    
    is_liked = False
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
        is_liked = False
    else:
        comment.likes.add(request.user)
        is_liked = True

    if is_liked and comment.dislikes.filter(id=request.user.id).exists():
        comment.dislikes.remove(request.user)

    context = {
        'comment': comment,
        'is_liked': is_liked,
    }
    
    if request.is_ajax():
        html = render_to_string('forum/comment_like_section.html', context, request=request)
        return JsonResponse({'form': html})

def like_reply(request):
    reply = get_object_or_404(Comment, id=request.POST.get('id'))

    is_liked = False
    if reply.likes.filter(id=request.user.id).exists():
        reply.likes.remove(request.user)
        is_liked = False
    else:
        reply.likes.add(request.user)
        is_liked = True

    if is_liked and reply.dislikes.filter(id=request.user.id).exists():
        reply.dislikes.remove(request.user)

    context = {
        'reply': reply,
        'is_liked': is_liked,
    }
    
    if request.is_ajax():
        html = render_to_string('forum/reply_like_section.html', context, request=request)
        return JsonResponse({'form': html})

def dislike_comment(request):
    comment = get_object_or_404(Comment, id=request.POST.get('id'))


    is_disliked = False
    if comment.dislikes.filter(id=request.user.id).exists():
        comment.dislikes.remove(request.user)
        is_disliked = False
    else:
        comment.dislikes.add(request.user)
        is_disliked = True

    if is_disliked and comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
    
    context = {
        'comment': comment,
        'is_disliked': is_disliked
    }

    if request.is_ajax():
        html = render_to_string('forum/comment_like_section.html', context, request=request)
        return JsonResponse({'form': html})

def dislike_reply(request):
    reply = get_object_or_404(Comment, id=request.POST.get('id'))


    is_disliked = False
    if reply.dislikes.filter(id=request.user.id).exists():
        reply.dislikes.remove(request.user)
        is_disliked = False
    else:
        reply.dislikes.add(request.user)
        is_disliked = True

    if is_disliked and reply.likes.filter(id=request.user.id).exists():
        reply.likes.remove(request.user)
    
    context = {
        'reply': reply,
        'is_disliked': is_disliked
    }

    if request.is_ajax():
        html = render_to_string('forum/reply_like_section.html', context, request=request)
        return JsonResponse({'form': html})

def save_post(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))
    saved_posts = Post.objects.filter(saves=request.user)
    
    is_saved = False
    if post.saves.filter(id=request.user.id).exists():
        post.saves.remove(request.user)
        messages.success(request, 'Post unsaved')
        is_saved = False
    else:
        post.saves.add(request.user)
        messages.success(request, 'Post saved')
        is_saved = True

    context = {
        'post': post,
        'is_saved': is_saved,
        'saved_posts': saved_posts,
    }
    
    if request.is_ajax():
        html = render_to_string('forum/like_section.html', context, request=request)
        html_count = render_to_string('forum/saved_posts_count.html', context, request=request)
        return JsonResponse({'form': html, 'count': html_count})

def follow_user(request, username):
    user = get_object_or_404(User, username=username)
    
    if request.user.profile.followings.filter(id=user.id).exists():
        request.user.profile.followings.remove(user)
        following = False
    else:
        request.user.profile.followings.add(user)
        following = True
    
    return JsonResponse({'status': following})


def join_community(request):
    community = get_object_or_404(Community, id=request.POST.get('id'))

    joined = False
    if community.members.filter(id=request.user.id).exists():
        community.members.remove(request.user)
        community.members_count -= 1
        community.save()
        messages.success(request, 'Successfully left ' + community.name)
        joined = False
    else:
        community.members.add(request.user)
        community.members_count += 1
        community.save()
        messages.success(request, 'Successfully joined ' + community.name)
        joined = True

    context = {
        'community': community,
        'joined': joined
    }

    if request.is_ajax():
        html = render_to_string('forum/join_community.html', context, request=request)
        return JsonResponse({'form': html})

