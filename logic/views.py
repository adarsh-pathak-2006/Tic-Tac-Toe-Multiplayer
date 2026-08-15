from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from logic.models import Game, Score
from logic.serializers import GameSerializer, GameCreateSerializer
from authentication.models import Profile

class GameListCreateAPI(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return GameCreateSerializer
        return GameSerializer

    def get_queryset(self):
        profile = self.request.user.profile
        return Game.objects.filter(Q(player1=profile) | Q(player2=profile))

    def perform_create(self, serializer):
        game = serializer.save(player1=self.request.user.profile)
        # Create a Score object automatically for the game
        Score.objects.create(game=game)

class GameRetrieveAPI(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GameSerializer

    def get_queryset(self):
        profile = self.request.user.profile
        return Game.objects.filter(Q(player1=profile) | Q(player2=profile))
