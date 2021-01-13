from django.urls import path
from .views import (
    PostDeleteView,
)
from . import views

urlpatterns = [
    path('', views.home, name='forum-home'),
    path('top/', views.home_top_posts, name='home-top-posts'),
    path('trending/', views.home_trending_posts, name='home-trending-posts'),
    path('post/new/', views.create_post_home, name='home-post'),
    path('<str:name>/post/new/', views.create_community_post, name='community-post'),
    path('communities/', views.community_list, name='communities'),
    path('community/new/', views.create_community, name='community-create'),
    path('community/<str:name>/', views.community_detail_new, name='community-detail-new'),
    path('community/<str:name>/trending/', views.community_detail_trending, name='community-detail-trending'),
    path('community/<str:name>/top/', views.community_detail_top, name='community-detail-top'),
    path('join/', views.join_community, name='join_community'),
    path('user/<str:username>/', views.user_posts, name='user-posts'),
    path('user/<str:username>/trending/', views.user_posts_trending, name='user-posts-trending'),
    path('user/<str:username>/top/', views.user_posts_top, name='user-posts-top'),
    path('user/<str:username>/notifications/', views.user_notifications, name='notifications'),
    path('saved/', views.saved, name='saved'),
    path('post/<int:id>/', views.post_detail, name='post-detail'),
    path('post/<int:pk>/delete/', views.delete_post, name='post-delete'),
    path('post/<int:pk>/update/', views.update_post, name='post-update'),
    path('like/', views.like_post, name='like_post'),
    path('dislike/', views.dislike_post, name='dislike_post'),
    path('save/', views.save_post, name='save_post'),
    path('like_comment/', views.like_comment, name='like_comment'),
    path('dislike_comment/', views.dislike_comment, name='dislike_comment'),
    path('like_reply/', views.like_reply, name='like_reply'),
    path('dislike_reply/', views.dislike_reply, name='dislike_reply'),
    path('notification/<int:post_id>/<int:comment_id>/', views.post_comment_notification, name='post-comment-notification'),
    path('follow_user/<str:username>/', views.follow_user, name='follow-user'),
]
