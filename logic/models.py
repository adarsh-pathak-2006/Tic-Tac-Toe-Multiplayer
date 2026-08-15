from django.db import models
from authentication.models import Profile

class Game(models.Model):
    player1=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='player1_in_game')
    player2=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='player2_in_game')
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"game btween {self.player1.name} and {self.player2.name}"

class Score(models.Model):
    game=models.OneToOneField(Game, on_delete=models.CASCADE, related_name='scores')
    player1_score=models.PositiveIntegerField(default=0)
    player2_score=models.PositiveIntegerField(default=0)
    winner=models.CharField(choices=[('PLAYER1', 'PLAYER1'), ('PLAYER2', 'PLAYER2'), ('DRAW', 'DRAW')], default='DRAW')

    def save(self,*args, **kwargs):
        if self.player1_score > self.player2_score:
            self.winner='PLAYER1'
        elif self.player2_score > self.player1_score:
            self.winner='PLAYER2'
        else:
            self.winner='DRAW'
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.game.__str__

class Move(models.Model):
    MOVE_CHOICES=[('H1V1','H1V1'), ('H2V1', 'H2V1'), ('H3V1', 'H3V1'), ('H1V2', 'H1V2'), ('H2V2', 'H2V2'), ('H3V2', 'H3V2'), ('H1V3', 'H1V3'), ('H2V3', 'H2V3'), ('H3V3', 'H3V3')]
    game=models.ForeignKey(Game, on_delete=models.CASCADE, related_name='moves_played')
    player=models.CharField(max_length=10, choices=[('PLAYER1', 'PLAYER1'), ('PLAYER2', 'PLAYER2')])
    move=models.CharField(max_length=4, choices=MOVE_CHOICES)
    played_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player} played {self.move}"
