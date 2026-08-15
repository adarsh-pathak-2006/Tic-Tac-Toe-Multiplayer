import json
from channels.generic.websocket import AsyncWebsocketConsumer
from logic.models import Move, Game, Score
from asgiref.sync import sync_to_async

WINNING_COMBINATIONS = [
    {'H1V1', 'H2V1', 'H3V1'},
    {'H1V2', 'H2V2', 'H3V2'},
    {'H1V3', 'H2V3', 'H3V3'},
    {'H1V1', 'H1V2', 'H1V3'},
    {'H2V1', 'H2V2', 'H2V3'},
    {'H3V1', 'H3V2', 'H3V3'},
    {'H1V1', 'H2V2', 'H3V3'},
    {'H3V1', 'H2V2', 'H1V3'},
]

class MoveSocket(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        
        if self.user.is_authenticated:
            self.profile_id = await self.get_profile_id(self.user)
            self.game = await Game.objects.select_related('player1', 'player2').aget(id=self.game_id)
            # Verify the user is part of the game
            if self.profile_id not in [self.game.player1_id, self.game.player2_id]:
                await self.close()
                return

            self.player_type = 'PLAYER1' if self.profile_id == self.game.player1_id else 'PLAYER2'
            
            await self.accept()
            self.game_group = f"game_group_{self.game_id}"
            await self.channel_layer.group_add(self.game_group, self.channel_name)
        else:
            await self.close()

    async def receive(self, text_data):
        message = json.loads(text_data)
        move_position = message.get("move")
        
        # Check if game is already over
        score = await Score.objects.aget(game=self.game)
        if score.winner != 'DRAW' or await self.is_draw(self.game):
            # Already over, score was DRAW but game might have actually ended as DRAW. Wait, Score defaults to DRAW.
            # We need to distinguish between initial DRAW and game over DRAW. Let's rely on move count for now.
            pass
            
        # Get all moves
        moves = await self.get_all_moves(self.game)
        
        if len(moves) == 9 or (score.winner != 'DRAW' and score.player1_score > 0 or score.player2_score > 0):
             await self.send(json.dumps({'error': 'Game is already over'}))
             return
             
        # Check turn
        if len(moves) % 2 == 0 and self.player_type != 'PLAYER1':
            await self.send(json.dumps({'error': 'Not your turn'}))
            return
        elif len(moves) % 2 == 1 and self.player_type != 'PLAYER2':
            await self.send(json.dumps({'error': 'Not your turn'}))
            return

        # Check if move is taken
        if move_position in [m.move for m in moves]:
            await self.send(json.dumps({'error': 'Cell already occupied'}))
            return

        # Create move
        await Move.objects.acreate(game=self.game, move=move_position, player=self.player_type)
        moves.append(Move(game=self.game, move=move_position, player=self.player_type))
        
        # Check win
        winner = self.check_winner(moves)
        is_draw = len(moves) == 9 and not winner
        
        if winner:
            score.winner = winner
            if winner == 'PLAYER1':
                score.player1_score = 1
            else:
                score.player2_score = 1
            await sync_to_async(score.save)()
        elif is_draw:
            score.winner = 'DRAW'
            await sync_to_async(score.save)()

        await self.channel_layer.group_send(self.game_group, {
            'type': 'move_update',
            'move': move_position,
            'player': self.player_type,
            'winner': winner,
            'is_draw': is_draw,
        })

    @sync_to_async
    def get_all_moves(self, game):
        return list(Move.objects.filter(game=game).order_by('played_at'))

    @sync_to_async
    def get_profile_id(self, user):
        return user.profile.id

    def check_winner(self, moves):
        player1_moves = {m.move for m in moves if m.player == 'PLAYER1'}
        player2_moves = {m.move for m in moves if m.player == 'PLAYER2'}
        
        for combo in WINNING_COMBINATIONS:
            if combo.issubset(player1_moves):
                return 'PLAYER1'
            if combo.issubset(player2_moves):
                return 'PLAYER2'
        return None
        
    @sync_to_async
    def is_draw(self, game):
        return Move.objects.filter(game=game).count() == 9

    async def move_update(self, event):
        await self.send(json.dumps({
            'move': event["move"],
            'player': event["player"],
            'winner': event.get("winner"),
            'is_draw': event.get("is_draw"),
        }))

    async def disconnect(self, close_code):
        if hasattr(self, 'game_group'):
            await self.channel_layer.group_discard(
                self.game_group,
                self.channel_name
            )
