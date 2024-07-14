import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import QueuingDetail, Message, Reply
from .serializers import QueuingSerializer, ITmessageSerializer, UserreplySerializer
from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
import asyncio

class QueuingConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def all_que(self):
        que = QueuingDetail.objects.all()
        que_serializer = QueuingSerializer(que, many=True)
        que_data = que_serializer.data
        return que_data

    async def connect(self):
        self.group_name = 'all_que'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_queuing_data()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_queuing_data(self):
        que = await self.all_que()
        await self.send(json.dumps({"que": que}))

    async def update(self, event):
        event['text']
        await self.send_queuing_data()

class MessageConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def all_messages(self, que_id):
        messages = Message.objects.filter(Que_num=que_id)
        messages_serializer = ITmessageSerializer(messages, many=True)
        messages_data = messages_serializer.data
        return messages_data

    @database_sync_to_async
    def save_message(self, que_id, message_content):
        queuing_detail = QueuingDetail.objects.get(pk=que_id)

    # Create the Message instance with the QueuingDetail instance
        message_details = Message.objects.create(
            Que_num=queuing_detail,
            Itmessage=message_content
        )
        # message_details.save()y
        return message_details

    async def connect(self):
        self.group_name = 'all_messages'
        que_id = self.scope['url_route']['kwargs']['que_id']
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_messages_data(que_id)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_messages_data(self, que_id):
        messages = await self.all_messages(que_id)
        await self.send(json.dumps({"messages": messages}))

    async def update(self, event):
        que_id = event['que_id']
        await self.send_messages_data(que_id)
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        que_id = self.scope['url_route']['kwargs']['que_id']
        message_content = data.get('message', '')

        # Save the new message to the database
        await self.save_message(que_id, message_content)

        # Send the updated message list to the WebSocket
        await self.send_messages_data(que_id)

        # Notify other group members about the new message
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'update',
                'que_id': que_id
            }
        )

class RepliesConsumer(AsyncWebsocketConsumer):
    connection_connect = True  # This is a class-level variable

    @database_sync_to_async
    def all_replies(self, que_id):
        replies = Reply.objects.filter(Que_num=que_id)
        replies_serializer = UserreplySerializer(replies, many=True)
        replies_data = replies_serializer.data
        return replies_data
    
    @database_sync_to_async
    def save_reply(self, que_id, message_content):
        queuing_detail = QueuingDetail.objects.get(pk=que_id)

        message_details = Reply.objects.create(
            Que_num=queuing_detail,
            user_reply=message_content
        )

        return message_details


    async def connect(self):
        self.group_name = 'all_replies'
        que_id = self.scope['url_route']['kwargs']['que_id']
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_replies_data(que_id)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_replies_data(self, que_id):
        replies = await self.all_replies(que_id)
        await self.send(json.dumps({"replies": replies}))

    async def update(self, event):
        que_id = event['que_id']
        await self.send_replies_data(que_id)
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        que_id = self.scope['url_route']['kwargs']['que_id']
        message_content = data.get('replies', '')

        # Save the new message to the database
        await self.save_reply(que_id, message_content)

        # Send the updated message list to the WebSocket
        await self.send_replies_data(que_id)

        # Notify other group members about the new message
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'update',
                'que_id': que_id
            }
        )

