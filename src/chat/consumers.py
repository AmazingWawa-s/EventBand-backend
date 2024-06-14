import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from event_band.utils import SECRET_KEY
from event_band.global_vars import All_conn_dict
import jwt
from entity.db import ChatMessageDB,UserDB
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
        print(data)
        await self.handle_example_message(data)

    async def handle_example_message(self, data):
        print(f'Received message: {data}')

        if data["eventId"]==-1 and data["receiverId"]==-1:
            global All_conn_dict
            decode_token=jwt.decode(data["userToken"],SECRET_KEY,algorithms="HS256")
            self.id=decode_token["userId"]
            All_conn_dict[self.id]=self
            
        else:
            time=datetime.fromtimestamp(float(data["timestamp"])/1000)
            chat=ChatMessage(self.id,data["content"],data["chatType"],time)
            if data["chatType"]==0:
                # 群聊
                chat.set({"chr_event_id":data["eventId"]})
                await send_to_group(data,data["eventId"],self.id)
            else:
                # 私聊
                chat.set({"chr_recv_id":data["receiverId"]})
                if data["receiverId"] in All_conn_dict:
                    await All_conn_dict[data["receiverId"]].send_notification(data,self.id)


    async def send_notification(self, dic,sender_id):
        if sender_id is not None:
            dbop=UserDB()
            dbop.selectById("user_name",sender_id)
            dic["sender_name"]=dbop.get()[0]["user_name"]
        result_dic={
            "type":"notification",
            "data":dic,
            "backend_send_time":time.asctime()
        }
        await self.send(text_data=json.dumps(result_dic))
        print(f'\n\nSending notification to id={self.id}: {result_dic}\n\n')
        



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

        time=datetime.fromtimestamp(float(data["timestamp"]))
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
        result_dic={
            "type":"chat",
            "data":dic,
            "backend_send_time":time.asctime()
        }
        await self.send(text_data=json.dumps(result_dic))
        print(f'\n\nSending chat to id={self.id}: {result_dic}\n\n')