import json
from chat_app.views import room
from channels.generic.websocket import WebsocketConsumer
from .models import ChatMessages
from asgiref.sync import async_to_sync


class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json["username"]

        ChatMessages(
            room=self.room_name, username=username, message=message).save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    def chat_message(self, event):
        message = event['message']
        username = event['username']

        self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
