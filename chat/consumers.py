

import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass
    
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            sender = text_data_json.get('sender')
            receiver = text_data_json.get('receiver')
            message_content = text_data_json.get('message_content')

            if sender and receiver and message_content:
                message = {
                    'message_content': message_content,
                    'sender': sender,
                    'receiver': receiver
                }

                # Send the message to both sender and receiver channels
                receiver_channel_name = f"user_{receiver}"
                
                await self.send(text_data=json.dumps(message))
                print(f"Sent message to sender {sender}: {message_content}")
                await self.channel_layer.send(
                    receiver_channel_name,
                    {
                        'type': 'chat.message',
                        'message_content': message_content,
                        'sender': sender
                    }
                )
                print(f"Sent message to receiver {receiver}: {message_content}")

                

            else:
                await self.send(text_data=json.dumps({'error': 'Invalid message format'}))
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({'error': 'Invalid JSON format'}))
    



    # async def receive(self,text_data):
    #     try:
    #         text_data_json = json.loads(text_data)
    #         sender= text_data_json.get('sender')
    #         receiver = text_data_json.get('receiver')
    #         message_content=text_data_json.get('message_content')
    #         # sender_type=text_data_json.get('sender_type')
    #         print(sender,receiver,message_content)


    #         if sender and receiver and message_content:
                
               

    #             await self.send(text_data=json.dumps({
    #                     'message_content':message_content,
    #                     'sender':sender,
    #                     'receiver':receiver
    #             }))
    #             print("message sent to sender")
    #             # Notify the receiver
    #             receiver_channel_name = f'receiver-{receiver}'
    #             print(receiver_channel_name,'why are you')
    #             await self.channel_layer.send(
    #                 receiver_channel_name,
    #                 {
    #                     'type': 'send_notification',
    #                     'message_content': message_content,
    #                     'sender': sender,
    #                     'receiver':receiver
    #                 }
    #             )
    #             print('notification send to receiver')
    #         else:
    #             await self.send(text_data=json.dumps({'error': 'Invalid message format'}))


                
            
    #     except json.JSONDecodeError:
    #         # Handle invalid JSON
    #         await self.send(text_data=json.dumps({'error': 'Invalid JSON format'}))



# await self.channel_layer.group_add(sender, self.channel_name)
                # await self.channel_layer.group_add(receiver, self.channel_name)

                # Store the message in your database or any other storage
                # ...