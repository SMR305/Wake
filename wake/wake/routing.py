from django.urls import path

from .consumers import ServerConsumer


websocket_urlpatterns = [
    path('ws/servers/', ServerConsumer.as_asgi()),
]