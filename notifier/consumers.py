from channels.generic.websocket import AsyncJsonWebsocketConsumer
import asyncio

class NoseyConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        # Checking if the User is logged in
        if self.scope['user'].is_anonymous:
            # Reject the connection
            self.close()
        else:
            self.user_room_name = str(self.scope['user'].id)
            await self.accept()
            await self.channel_layer.group_add(self.user_room_name, self.channel_name)
            print(self.scope['user'])
            print(f"Added {self.user_room_name} channel to group")
    
    async def disconnect(self, close_code):
        print(str(self.scope['user']) + " disconnected")

    async def user_notification(self, event):
        await self.send_json(event)
        print(f"Created notification: {event} at {self.channel_name}")

    async def chat_notification(self, event):
        await self.send_json(event)
        print(f"Created chat notification: {event}")