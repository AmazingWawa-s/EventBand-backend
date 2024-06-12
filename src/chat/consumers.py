import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from event_band.utils import All_conn_dict,SECRET_KEY
import jwt

User = get_user_model()

class NotificationConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.id=-1

    async def connect(self):
        self.user = self.scope['user']
        print(f"User: {self.user}")

        self.group_name = f'notifications_{self.user.id}'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        global All_conn_dict
        del All_conn_dict[self.id]
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        await self.handle_example_message(data)

    async def handle_example_message(self, data):
        print(f'Received message: {data}')
        # Example logic to broadcast message back to the client

        global All_conn_dict
        decode_token=jwt.decode(data["userToken"],SECRET_KEY,algorithms="HS256")
        self.id=decode_token["userId"]
        All_conn_dict[self.id]=self

        await self.send_notification({
            'type': 'send_notification',
            'message': data
        })
    
    async def send_notification(self, dic):
        message = dic['message']
        print(f'Sending notification: {message}')
        await self.send(text_data=json.dumps({
            'title': 'Notification',
            'body': message,
            'timestamp': '2024-06-12T14:30:00Z'
        }))
