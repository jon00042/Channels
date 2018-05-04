import json
from django.conf import settings
from channels.generic.websocket import JsonWebsocketConsumer
from pprint import pprint

import django

class ChatConsumer(JsonWebsocketConsumer):

    def connect(self):
        pprint(self.scope['session'].items())
        if ('user_id' in self.scope['session']):
            self.accept()
            print('connected')
        else:
            self.close()
            print('no valid session')

    def receive_json(self, content):
        pass

    def disconnect(self, close_code):
        pass

