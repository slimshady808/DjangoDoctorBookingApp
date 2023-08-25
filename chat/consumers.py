

import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import UserToDoctorMessage, DoctorToUserMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass
    @database_sync_to_async
    def save_message_to_db(self, sender, receiver, message_content, sender_type):
        if sender_type=='user':
            message_instance=UserToDoctorMessage(sender=sender, receiver=receiver, message_content=message_content)
        else:
            message_instance=DoctorToUserMessage(sender=sender, receiver=receiver, message_content=message_content)
        if message_instance:
            message_instance.save()

        



    async def receive(self,text_data):
        try:
            text_data_json = json.loads(text_data)
            sender= text_data_json.get('sender')
            receiver = text_data_json.get('receiver')
            message_content=text_data_json.get('message_content')
            sender_type=text_data_json.get('sender_type')
            print(sender,receiver,message_content,sender_type)


            if sender and receiver and message_content and sender_type:
                #save the message to the database
                await self.save_message_to_db(sender, receiver, message_content, sender_type)
               

                await self.send(text_data=json.dumps({
                        'message':message_content,
                        'sender':sender
                }))
            else:
                await self.send(text_data=json.dumps({'error': 'Invalid message format'}))


                
            
        except json.JSONDecodeError:
            # Handle invalid JSON
            await self.send(text_data=json.dumps({'error': 'Invalid JSON format'}))


    # async def receive(self, text_data):
    #     try:
    #         text_data_json = json.loads(text_data)
    #         message = text_data_json.get('message')
            
    #         if message:
    #             print("Received message:", message)  # Print the received message
    #             await self.send(text_data=json.dumps({'message': message}))
    #         else:
    #             await self.send(text_data=json.dumps({'error': 'Invalid message format'}))
    #     except json.JSONDecodeError:
    #         # Handle invalid JSON
    #         await self.send(text_data=json.dumps({'error': 'Invalid JSON format'}))

    # async def receive(self, text_data):
    #     try:
    #         text_data_json = json.loads(text_data)
    #         message = text_data_json['message']
            
    #     except json.JSONDecodeError:
    #         # Handle invalid JSON
    #         print("Invalid JSON format received")
            
    #         return

    #     # Send the message back to the WebSocket
    #     await self.send(text_data=json.dumps({'message': message}))
        



# # chat/consumers.py

# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Accept the WebSocket connection
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Perform cleanup when the WebSocket closes
#         pass

#     async def receive(self, text_data):
#         # Handle incoming WebSocket messages
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Broadcast the message to other connected users
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))
