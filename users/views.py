from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models import F
from django.db.models import Count
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from forum.models import Post, Community, Comment, Notification, ChatNotification
from chat.models import ChatRoom, ChatMessage

class LoginView(auth_views.LoginView):
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section']  = 'Log In'
        context['section_img'] = '/media/login.svg'
        context['title'] = 'Login'
        return context

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in!')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form, 'section': 'Register', 'section_img': '/media/registered.svg', 'title': 'Register'})

@login_required
def profile(request):
    posts = Post.objects.filter(author=request.user).order_by('-date_posted')

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    communities = Community.objects.filter(members=request.user)
    
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

    user =  User.objects.get(username=request.user)
    post_likes = 0
    post_dislikes = 0
    comment_likes = 0 
    comment_dislikes = 0
    user_comments = Comment.objects.filter(user=user)
    user_posts = Post.objects.filter(author=user)
    
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

        chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-latest_message_date')
        user_chat_rooms = []
        for user_chat_room in chat_rooms:
            count = ChatNotification.objects.filter(recipient=request.user, chat_room=user_chat_room, read=False).count()
            user_chat_rooms.append([user_chat_room, count])

    context = {
        'space_points': space_points,
        'u_form': u_form,
        'p_form': p_form,
        'posts': posts,
        'communities': communities,
        'personal_communities': communities,
        'notifications': notifications,
        'user_chat_rooms': user_chat_rooms,
        'user': user,
        'section': 'Profile',
        'section_img': "/media/user.svg",
        'title': 'Profile',
    }

    if request.is_ajax():
        if request.method == 'GET' and request.GET.get('page') is None:

            ajax_context = context
            html = render_to_string('users/profile_ajax.html', ajax_context, request=request)
            right_html = render_to_string('users/users_communities.html', ajax_context, request=request)

            return JsonResponse({'form': html, 'user_info': right_html})
        
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST,
                                        request.FILES,
                                        instance=request.user.profile)

            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, 'Your account has been updated!')
                return redirect('profile')
            

    return render(request, 'users/profile.html', context)

@login_required
def profile_trending_posts(request):
    user_posts = Post.objects.filter(author=request.user)
    for post in user_posts:
        total_points = post.likes.count() + post.dislikes.count() + post.post.count()
        post.trending_points = F('trending_points') + total_points
        post.save()

    posts = Post.objects.filter(author=request.user).order_by('-trending_points')

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    communities = Community.objects.filter(members=request.user)
    
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

    user =  User.objects.get(username=request.user)
    post_likes = 0
    post_dislikes = 0
    comment_likes = 0 
    comment_dislikes = 0
    user_comments = Comment.objects.filter(user=user)
    user_posts = Post.objects.filter(author=user)
    
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

        chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-latest_message_date')
        user_chat_rooms = []
        for user_chat_room in chat_rooms:
            count = ChatNotification.objects.filter(recipient=request.user, chat_room=user_chat_room, read=False).count()
            user_chat_rooms.append([user_chat_room, count])

    context = {
        'space_points': space_points,
        'u_form': u_form,
        'p_form': p_form,
        'posts': posts,
        'communities': communities,
        'personal_communities': communities,
        'notifications': notifications,
        'user_chat_rooms': user_chat_rooms,
        'user': user,
        'section': 'Profile',
        'section_img': "/media/user.svg",
        'title': 'Profile',
    }

    if request.is_ajax():
        if request.method == 'GET' and request.GET.get('page') is None:

            ajax_context = context
            html = render_to_string('users/profile_ajax.html', ajax_context, request=request)
            right_html = render_to_string('users/users_communities.html', ajax_context, request=request)

            return JsonResponse({'form': html, 'user_info': right_html})

    return render(request, 'users/profile_trending_posts.html', context)

@login_required
def profile_top_posts(request):
    posts = Post.objects.filter(author=request.user).annotate(num_likes=Count('likes')).order_by('-num_likes')

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    communities = Community.objects.filter(members=request.user)
    
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

    user =  User.objects.get(username=request.user)
    post_likes = 0
    post_dislikes = 0
    comment_likes = 0 
    comment_dislikes = 0
    user_comments = Comment.objects.filter(user=user)
    user_posts = Post.objects.filter(author=user)
    
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

        chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-latest_message_date')
        user_chat_rooms = []
        for user_chat_room in chat_rooms:
            count = ChatNotification.objects.filter(recipient=request.user, chat_room=user_chat_room, read=False).count()
            user_chat_rooms.append([user_chat_room, count])

    context = {
        'space_points': space_points,
        'u_form': u_form,
        'p_form': p_form,
        'posts': posts,
        'communities': communities,
        'personal_communities': communities,
        'notifications': notifications,
        'user_chat_rooms': user_chat_rooms,
        'user': user,
        'section': 'Profile',
        'section_img': "/media/user.svg",
        'title': 'Profile',
    }

    if request.is_ajax():
        if request.method == 'GET' and request.GET.get('page') is None:

            ajax_context = context
            html = render_to_string('users/profile_ajax.html', ajax_context, request=request)
            right_html = render_to_string('users/users_communities.html', ajax_context, request=request)

            return JsonResponse({'form': html, 'user_info': right_html})

    return render(request, 'users/profile_top_posts.html', context)