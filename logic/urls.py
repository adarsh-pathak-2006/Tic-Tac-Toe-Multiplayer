from django.urls import path
from logic.views import GameListCreateAPI, GameRetrieveAPI

urlpatterns = [
    path('games/', GameListCreateAPI.as_view(), name='game_list_create'),
    path('games/<int:pk>/', GameRetrieveAPI.as_view(), name='game_retrieve'),
]
