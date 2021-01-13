from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, re_path
from django.conf.urls import url
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from notifier.consumers import NoseyConsumer
from chat.consumers import ChatConsumer

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url("notifications/", NoseyConsumer),
            url(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer),
        ])
    ),
})