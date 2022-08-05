import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.db.models import QuerySet

from .models import Message, ChatRoom, ChatRoomUser


async def get_user_by_name(name) -> User:
    user = await sync_to_async(User.objects.get)(username=name)
    return user


async def get_room_by_name(name) -> ChatRoom:
    room = await sync_to_async(ChatRoom.objects.get)(name=name)
    return room


async def get_last_messages(room_name, numer=None):
    room = await get_room_by_name(room_name)
    queryset: QuerySet = await sync_to_async(Message.objects.filter)(room_id=room.id)
    queryset = queryset.order_by(
        '-timestamp'
    )[:numer or 3].values('body', 'user__username', 'timestamp')
    return await sync_to_async(list)(queryset)


async def add_user_in_room(username, room_name):
    room = await get_room_by_name(room_name)
    if isinstance(username, User):
        user = username
    else:
        user = await get_user_by_name(username)
    await sync_to_async(ChatRoomUser.objects.create)(user=user, room=room)
    query = await sync_to_async(ChatRoomUser.objects.filter)(user=user, room=room)
    return await sync_to_async(query.count)()


async def remove_user_from_room(username, room_name):
    room = await get_room_by_name(room_name)
    if isinstance(username, User):
        user = username
    else:
        user = await get_user_by_name(username)
    chat_room_user = await sync_to_async(ChatRoomUser.objects.filter)(user=user, room=room)
    chat_room_user = await sync_to_async(chat_room_user.first)()
    if chat_room_user:
        await sync_to_async(chat_room_user.delete)()
    query = await sync_to_async(ChatRoomUser.objects.filter)(user=user, room=room)
    return await sync_to_async(query.count)()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        username = self.scope['user'].username
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        messages = await get_last_messages(self.room_name)
        messages = messages[::-1]
        for message in messages:
            await self.send(text_data=json.dumps({'message': {
                'body': message['body'],
                'user': message['user__username'],
                # 'timestamp': message['timestamp'],
            }}))
        if await add_user_in_room(username, self.room_name) == 1:
            await self.send_message_to_chatroom(
                f'{username} has joined the chat')

    async def disconnect(self, close_code):
        # Leave room group
        user = self.scope['user']
        if await remove_user_from_room(user, self.room_name) == 0:
            await self.send_message_to_chatroom(
                f'{user.username} has left the chat')
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def get_user_list(self):
        users_query = await sync_to_async(ChatRoomUser.objects.filter)(room__name=self.room_name)
        users_query = await sync_to_async(users_query.distinct)()
        user_list = await sync_to_async(users_query.values_list)('user__username', flat=True)
        return await sync_to_async(list)(user_list)

    async def send_message_to_chatroom(self, message, username=None):
        user_list = await self.get_user_list()
        data = {
            'body': message,
            'user_list': user_list,
        }
        if username:
            data['user'] = username

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': data,
            }
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['user']
        # Send message to room group
        await self.send_message_to_chatroom(message, username)
        user = await get_user_by_name(username)
        room = await get_room_by_name(self.room_name)
        await sync_to_async(Message.objects.create)(body=message, user=user, room=room)

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
