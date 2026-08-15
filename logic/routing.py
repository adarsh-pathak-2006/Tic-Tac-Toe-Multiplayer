from django.urls import path
from logic.consumer import MoveSocket

url_patterns=[
    path('ws/game/<int:game_id>', MoveSocket.as_asgi(), name='move_socket'),
]