

import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass
    



    async def receive(self,text_data):
        try:
            text_data_json = json.loads(text_data)
            sender= text_data_json.get('sender')
            receiver = text_data_json.get('receiver')
            message_content=text_data_json.get('message_content')
            # sender_type=text_data_json.get('sender_type')
            print(sender,receiver,message_content)


            if sender and receiver and message_content:
                
               

                await self.send(text_data=json.dumps({
                        'message_content':message_content,
                        'sender':sender,
                        'receiver':receiver
                }))
                print("message sent to sender")
                # Notify the receiver
                receiver_channel_name = f'receiver-{receiver}'
                print(receiver_channel_name,'why are you')
                await self.channel_layer.send(
                    receiver_channel_name,
                    {
                        'type': 'send_notification',
                        'message_content': message_content,
                        'sender': sender,
                        'receiver':receiver
                    }
                )
                print('notification send to receiver')
            else:
                await self.send(text_data=json.dumps({'error': 'Invalid message format'}))


                
            
        except json.JSONDecodeError:
            # Handle invalid JSON
            await self.send(text_data=json.dumps({'error': 'Invalid JSON format'}))

# class ReceiverConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         receiver_id = self.scope['url_route']['kwargs']['receiver_id']
#         self.group_name = f'receiver-{receiver_id}'

#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#     async def send_notification(self, event):
#         message_content = event['message_content']
#         sender = event['sender']

#         await self.send(text_data=json.dumps({
#             'message_content': message_content,
#             'sender': sender
#         }))

    