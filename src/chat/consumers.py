import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from event_band.utils import SECRET_KEY
from event_band.global_vars import All_conn_dict
import jwt
from entity.db import ChatMessageDB
from entity.message import ChatMessage
from chat.views import send_to_group
import time
from datetime import datetime

User = get_user_model()

class NotificationConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.id=-1

    async def connect(self):
        self.user = self.scope['user']

        self.group_name = f'Notification_{self.user.id}'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        global All_conn_dict
        if self.id in All_conn_dict:
            del All_conn_dict[self.id]
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        await self.handle_message(data)

    async def handle_message(self, data):
        print(f'Received message: {data}')

        global All_conn_dict
        decode_token=jwt.decode(data["userToken"],SECRET_KEY,algorithms="HS256")
        self.id=decode_token["userId"]
        All_conn_dict[self.id]=self


    async def send_notification(self, dic):
        dic["backend_send_time"]=time.asctime()
        await self.send(text_data=json.dumps(dic))
        print(f'\n\n\nSending notification to id={self.id}: {dic}\n\n\n')
        



class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.id=-1

    async def connect(self):
        self.user = self.scope['user']

        self.group_name = f'chat_{self.user.id}'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        global All_conn_dict
        if self.id in All_conn_dict:
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

        global All_conn_dict
        decode_token=jwt.decode(data["userToken"],SECRET_KEY,algorithms="HS256")
        self.id=decode_token["userId"]
        All_conn_dict[self.id]=self

        time=datetime.fromtimestamp(float(data["time"]))
        chat=ChatMessage(self.id,data["content"],data["chatType"],time)
        if data["chatType"]==0:
            # 群聊
            chat.set({"chr_event_id":data["eventId"]})
            await send_to_group(data,data["eventId"])
        else:
            # 私聊
            chat.set({"chr_recv_id":data["receiverId"]})
            if data["receiverId"] in All_conn_dict:
                await All_conn_dict[data["receiverId"]].send_notification(data)

    # async def handle_example_message(self, data):
    #     print(f'Received message: {data}')

    #     global All_conn_dict

    #     temp_dict={"data":data}
    #     await self.send_notification(temp_dict)


    async def send_notification(self, dic):
        dic["backend_send_time"]=time.asctime()
        print(f'Sending chat to id={self.id}: {dic}')
        await self.send(text_data=json.dumps(dic))