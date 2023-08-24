import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass


    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message')
            
            if message:
                print("Received message:", message)  # Print the received message
                await self.send(text_data=json.dumps({'message': message}))
            else:
                await self.send(text_data=json.dumps({'error': 'Invalid message format'}))
        except json.JSONDecodeError:
            # Handle invalid JSON
            await self.send(text_data=json.dumps({'error': 'Invalid JSON format'}))

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
