from rest_framework.serializers import ModelSerializer
from logic.models import Game, Score, Move
from authentication.serializers import ProfileGetSerializer

class ScoreSerializer(ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'

class MoveSerializer(ModelSerializer):
    class Meta:
        model = Move
        fields = '__all__'

class GameSerializer(ModelSerializer):
    player1 = ProfileGetSerializer(read_only=True)
    player2 = ProfileGetSerializer(read_only=True)
    scores = ScoreSerializer(read_only=True)
    moves_played = MoveSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ['id', 'player1', 'player2', 'created_on', 'scores', 'moves_played']

class GameCreateSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'player2']
        read_only_fields = ['id']
