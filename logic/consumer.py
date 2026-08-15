import json
from channels.generic.websocket import AsyncWebsocketConsumer
from logic.models import Move, Game

class MoveSocket(AsyncWebsocketConsumer):
    async def connect(self):
        self.user=self.scope['user']
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        if self.user.is_authenticated:
            await self.accept()
            self.game_group=f"game_group_{self.game_id}"
            await self.channel_layer.group_add(self.game_group, self.channel_name)
        else:
            await self.close()

    async def receive(self, text_data):
        message=json.loads(text_data)
        move=message.get("move")
        player=message.get("player")
        game_data=await Game.objects.aget(id=self.game_id)
        await Move.objects.acreate(game=game_data, move=move, player=player)

        await self.channel_layer.group_send(self.game_group, {
            'type':'move_update',
            'move':move,
            'player':player,
        })

    async def move_update(self, event):
        await self.send(json.dumps({
            'move':event["move"],
            'player':event["player"]
        }))

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.game_group,
            self.channel_name
        )
