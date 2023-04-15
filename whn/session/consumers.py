import channels.generic.websocket


class LobbyConsumer(channels.generic.websocket.AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
