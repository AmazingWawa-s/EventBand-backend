import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
   
    async def connect(self):
        print("here")
        self.user = self.scope['user']
        print(self.user)
        
        if self.user.is_authenticated:
            self.group_name = f'notifications_{self.user.id}'
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        # 处理接收到的数据
        message_type = data.get('type')
        message_content = data.get('message')

        # 根据消息类型进行不同的处理
        if message_type == 'example_type':
            # 处理特定类型的消息
            await self.handle_example_message(message_content)

    async def handle_example_message(self, message_content):
        print(f'Received message: {message_content}')
        # 在这里执行任何需要的逻辑，例如将消息存储到数据库或发送给其他用户

    async def send_notification(self, event):
        message = event['message']
        await self.send(text_data=message)
