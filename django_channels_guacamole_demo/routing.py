from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from .consumers import GuacamoleWebSocketConsumer


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws', GuacamoleWebSocketConsumer.as_asgi()),
        ])
    ),
})
