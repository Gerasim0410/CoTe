import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_app.settings')


def get_websocket_urlpatterns():
    from quiz_app.urls import websocket_urlpatterns
    return websocket_urlpatterns


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            get_websocket_urlpatterns()
        )
    ),
})
