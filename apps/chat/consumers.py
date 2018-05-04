import json
from asgiref.sync import async_to_sync
from django.conf import settings
from channels.generic.websocket import JsonWebsocketConsumer
from pprint import pprint

import django

class ChatConsumer(JsonWebsocketConsumer):

    def connect(self):
        if ('user_id' in self.scope['session']):
            self.accept()
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            attach_to = async_to_sync(self.channel_layer.group_add)
            attach_to(self.room_name, self.channel_name)
            broadcast_to = async_to_sync(self.channel_layer.group_send)
            broadcast_to(self.room_name, {
                'type': 'send.notification',
                'success': True,
                'notification': '{} has joined the room'.format(self.scope['session']['username']),
            })
            self.send_json({'success': True })
        else:
            self.close()
            print('no valid session')

    def receive_json(self, content):
        broadcast_to = async_to_sync(self.channel_layer.group_send)
        broadcast_to(self.room_name, {
            'type': 'send.message',
            'success': True,
            'message': content['message'],
            'username': self.scope['session']['username'],
        })

    def disconnect(self, close_code):
        broadcast_to = async_to_sync(self.channel_layer.group_send)
        broadcast_to(self.room_name, {
            'type': 'send.notification',
            'success': True,
            'notification': '{} has left the room'.format(self.scope['session']['username']),
        })

    #####################

    def send_message(self, event):
        self.send_json({
            'success': event['success'],
            'message': event['message'],
            'username': event['username'],
        })

    def send_notification(self, event):
        self.send_json({
            'success': event['success'],
            'notification': event['notification'],
        })

