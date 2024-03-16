import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer








class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'public_room'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({ 'message': event['message'] }))

async def send_message_to_user(self, recipient_username, message):
    sender_username = self.scope['user'].username

    
    sanitized_recipient_username = self.sanitize_group_name(recipient_username)

    
    group_name = f"{sanitized_recipient_username}_{sender_username}"

    
    await self.channel_layer.group_add(
        group_name,
        self.channel_name
    )

    
    await self.channel_layer.group_send(
        group_name,
        {
            'type': 'chat.message',
            'message': message,
            'sender_username': sender_username,
        }
    )

def sanitize_group_name(self, name):
    """
    Sanitize the group name to ensure it is a valid Unicode string
    with length < 100 containing only ASCII alphanumerics,
    hyphens, underscores, or periods.
    """
    
    sanitized_name = ''.join(c if c.isalnum() or c in '-_.' else '_' for c in name)


    sanitized_name = sanitized_name[:99]

    
    if not sanitized_name[0].isalnum():
        sanitized_name = 'group_' + sanitized_name

    return sanitized_name











