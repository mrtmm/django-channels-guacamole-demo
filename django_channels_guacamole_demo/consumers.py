import asyncio

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from guacamole.client import GuacamoleClient

from django.conf import settings


class GuacamoleWebSocketConsumer(AsyncWebsocketConsumer):
    client = None
    task = None

    async def connect(self):
        """
        Initiate the GuacamoleClient and create a connection to it.
        """
        self.client = GuacamoleClient(settings.GUACD_HOST, settings.GUACD_PORT)
        self.client.handshake(protocol=settings.PROTOCOL,
                              hostname=settings.HOST,
                              port=settings.PORT,
                              username=settings.USER,
                              password=settings.PASSWORD,
                              private_key=settings.PRIVATE_KEY)

        if self.client.connected:
            # start receiving data from GuacamoleClient
            self.task = asyncio.create_task(self.open())

            # Accept connection
            await self.accept(subprotocol='guacamole')
        else:
            await self.close()

    async def disconnect(self, code):
        """
        Close the GuacamoleClient connection on WebSocket disconnect.
        """
        self.task.cancel()
        await sync_to_async(self.client.close)()

    async def receive(self, text_data=None, bytes_data=None):
        """
        Handle data received in the WebSocket, send to GuacamoleClient.
        """
        if text_data is not None:
            self.client.send(text_data)

    async def open(self):
        """
        Receive data from GuacamoleClient and pass it to the WebSocket
        """
        while True:
            content = await sync_to_async(self.client.receive)()
            if content:
                await self.send(text_data=content)
