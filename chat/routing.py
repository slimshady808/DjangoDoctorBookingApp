# chat/routing.py

from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
    #re_path(r'ws/receiver/(?P<receiver_id>\d+)/$', consumers.ReceiverConsumer.as_asgi()),
]
