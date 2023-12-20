import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage  # Import your ChatMessage model here
from .serializer import ChatSerializer  # Import your ChatSerializer here
from accounts.models import AccountUser


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs'].get('room_name') 
        if self.room_name:

          await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = text_data_json['sender_id']
        receiver_id = text_data_json['receiver_id']

        try:
            sender = AccountUser.objects.get(id=sender_id)
            receiver = AccountUser.objects.get(id=receiver_id)

            chat_message = ChatMessage.objects.create(
                sender=sender,
                receiver=receiver,
                message=message
            )

            serializer = ChatSerializer(chat_message)

            if self.room_name:   # Broadcast the received message to other connected users in the group
               await self.channel_layer.group_send(
                   self.room_group_name,
                   {
                      'type': 'chat_message',
                      'message': serializer.data,
                   }
            )
        except AccountUser.DoesNotExist:
            pass

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))





























# import json
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer
# from .models import Chat, Message
# from .serializer import ChatSerializer, MessageSerializer

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_id = self.scope['url_route']['kwargs']['room_id']
#         self.room_group_name = f'chat_{self.room_id}'

#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )

#         self.accept()

#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

#     # Receive message from WebSocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Save message to database (assuming your Message model is appropriately set)
#         chat = Chat.objects.get(pk=self.room_id)
#         sender = self.scope["user"]
#         Message.objects.create(chat=chat, sender=sender, content=message)

#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'username': sender.username  # Send the username along with the message
#             }
#         )

#     # Receive message from room group
#     def chat_message(self, event):
#         message = event['message']
#         username = event['username']

#         # Send message to WebSocket
#         self.send(text_data=json.dumps({
#             'message': message,
#             'username': username
#         }))























# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.chat_id = self.scope['url_route']['kwargs']['chat_id']
#         # Logic for connecting to the WebSocket
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Logic for disconnecting from the WebSocket
#         pass

#     async def receive(self, text_data):
#         message = json.loads(text_data)
#         # Logic for handling incoming messages
#         await self.send(text_data=json.dumps({
#             'message': message['message']  # Modify this based on your message format
#         }))
































# import json
# from channels.db import database_sync_to_async
# from channels.generic.websocket import AsyncWebsocketConsumer
# from chat.models import ChatRoom, ChatMessage
# from accounts.models import AccountUser

# class ChatConsumer(AsyncWebsocketConsumer):
# 	def getUser(self, userId):
# 		return AccountUser.objects.get(id=userId)

# 	# def getOnlineUsers(self):
# 	# 	onlineUsers = OnlineUser.objects.all()
# 	# 	return [onlineUser.user.id for onlineUser in onlineUsers]

# 	# def addOnlineUser(self, user):
# 	# 	try:
# 	# 		OnlineUser.objects.create(user=user)
# 	# 	except:
# 	# 		pass

# 	# def deleteOnlineUser(self, user):
# 	# 	try:
# 	# 		OnlineUser.objects.get(user=user).delete()
# 	# 	except:
# 	# 		pass

# 	def saveMessage(self, message, userId, roomId):
# 		userObj = AccountUser.objects.get(id=userId)
# 		chatObj = ChatRoom.objects.get(roomId=roomId)
# 		chatMessageObj = ChatMessage.objects.create(
# 			chat=chatObj, user=userObj, message=message
# 		)
# 		return {
# 			'action': 'message',
# 			'user': userId,
# 			'roomId': roomId,
# 			'message': message,
# 			'userImage': userObj.image.url,
# 			'userName': userObj.first_name + " " + userObj.last_name,
# 			'timestamp': str(chatMessageObj.timestamp)
# 		}

# 	async def sendOnlineUserList(self):
# 		onlineUserList = await database_sync_to_async(self.getOnlineUsers)()
# 		chatMessage = {
# 			'type': 'chat_message',
# 			'message': {
# 				'action': 'onlineUser',
# 				'userList': onlineUserList
# 			}
# 		}
# 		await self.channel_layer.group_send('onlineUser', chatMessage)

# 	async def connect(self):
# 		self.userId = self.scope['url_route']['kwargs']['userId']
# 		self.userRooms = await database_sync_to_async(
# 			list
# 		)(ChatRoom.objects.filter(member=self.userId))
# 		for room in self.userRooms:
# 			await self.channel_layer.group_add(
# 				room.roomId,
# 				self.channel_name
# 			)
# 		await self.channel_layer.group_add('onlineUser', self.channel_name)
# 		self.user = await database_sync_to_async(self.getUser)(self.userId)
# 		await database_sync_to_async(self.addOnlineUser)(self.user)
# 		await self.sendOnlineUserList()
# 		await self.accept()

# 	async def disconnect(self, close_code):
# 		await database_sync_to_async(self.deleteOnlineUser)(self.user)
# 		await self.sendOnlineUserList()
# 		for room in self.userRooms:
# 			await self.channel_layer.group_discard(
# 				room.roomId,
# 				self.channel_name
# 			)

# 	async def receive(self, text_data):
# 		text_data_json = json.loads(text_data)
# 		action = text_data_json['action']
# 		roomId = text_data_json['roomId']
# 		chatMessage = {}
# 		if action == 'message':
# 			message = text_data_json['message']
# 			userId = text_data_json['user']
# 			chatMessage = await database_sync_to_async(
# 				self.saveMessage
# 			)(message, userId, roomId)
# 		elif action == 'typing':
# 			chatMessage = text_data_json
# 		await self.channel_layer.group_send(
# 			roomId,
# 			{
# 				'type': 'chat_message',
# 				'message': chatMessage
# 			}
# 		)

# 	async def chat_message(self, event):
# 		message = event['message']
# 		await self.send(text_data=json.dumps(message))















#     # app/consumers.py
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Check if the user is admin or regular user and join appropriate room

#         if self.scope.get('user') and self.scope['user'].is_authenticated:
#             user = self.scope["user"]
#             email = user.email
           
#             await self.accept()
#         else:
#             # Handle unauthenticated users - reject the connection or handle as needed
#             await self.close()
#         if user.is_superuser:
#             await self.channel_layer.group_add("admin", self.channel_name)
#         else:
#             await self.channel_layer.group_add("users", self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         if self.scope['user'].is_superuser:
#             await self.channel_layer.group_discard("admin", self.channel_name)
#         else:
#             await self.channel_layer.group_discard("users", self.channel_name)

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']

#         # Broadcast messages to respective groups (users or admin)
#         if self.scope['user'].is_superuser:
#             await self.channel_layer.group_send("users", {"type": "chat_message", "message": message})
#         else:
#             await self.channel_layer.group_send("admin", {"type": "chat_message", "message": message})

#     async def chat_message(self, event):
#         message = event['message']
#         await self.send(text_data=json.dumps({'message': message}))



















# # chat/consumers.py
# import json
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import ChatMessage
# from accounts.models import AccountUser

# from channels.db import database_sync_to_async

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.appointment_id = self.scope['url_route']['kwargs']['appointment_id']
#         self.appointment = await self.get_appointment_instance(self.appointment_id)

#         await self.channel_layer.group_add(
#             f'chat_{self.appointment_id}',
#             self.channel_name
#         )

#         await self.accept()
        
#         # Fetch existing messages and send them to the connected client
#         existing_messages = await self.get_existing_messages()
#         for message in existing_messages:
#             await self.send(text_data=json.dumps({
#                 'message': message['message'],
#             }))

#     @database_sync_to_async
#     def get_existing_messages(self):
#         # Assuming you have a ChatMessage model with a 'message' field
#         messages = ChatMessage.objects.filter(appointment=self.appointment)
#         return [{'message': message.message} for message in messages]

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             f'chat_{self.appointment_id}',
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']

#         await self.save_message(message)

#         await self.channel_layer.group_send(
#             f'chat_{self.appointment_id}',
#             {
#                 'type': 'chat.message',
#                 'data': data,
#             }
#         )

#     async def chat_message(self, event):
#         message = event['data']['message']

#         await self.send(text_data=json.dumps({
#             'message': message,
#         }))

#     @classmethod
#     async def send_chat_message(cls, appointment_id, message):
#         await cls.send_group(f'chat_{appointment_id}', {
#             'type': 'chat.message',
#             'message': message,
#         })


#     async def save_message(self, message):
#         sender = await self.get_user_instance(self.appointment.user_id)
#         receiver = await self.get_doctor_instance(self.appointment.doctor_id)

#         await self.save_message_to_db(sender, receiver, message)

#     @database_sync_to_async
#     def save_message_to_db(self, sender, receiver, message):
#         ChatMessage.objects.create(
#             sender=sender,
#             receiver=receiver,
#             message=message,
#             appointment=self.appointment
#         )

#     @database_sync_to_async
#     def get_user_instance(self, user_id):
#         try:
#             user = AccountUser.objects.get(id=user_id)
#             return user
#         except AccountUser.DoesNotExist:
#             print("Failed to find the user")





  




















# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']

#         # Process received message
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))































# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import sync_to_async
# from django.utils.timesince import timesince

# from .serializer import UserSerializer
# from .models import ChatMessage
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_id = self.scope['url_route']['kwargs']['room_id']
#         self.room_group_name = f"chat_{self.room_id}"
#         # Add the channel to the room's group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#         # Accept the WebSocket connection
#         await self.accept()
#         # Send a connection message to the client

#     async def disconnect(self, close_code):
#         # Remove the channel from the room's group upon disconnect
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         user = self.scope["user"]
#         user_serializer = UserSerializer(user)
#         email = user_serializer.data['email']

#         new_message = await self.create_message(self.room_id, message, email)
        
#         # Send the received message to the room's group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'room_id': self.room_id,
#                 'sender_email': email,
#                 'created': timesince(new_message.timestamp),
#             }
#         )

#     async def chat_message(self, event):
#         message = event['message']
#         room_id = event['room_id']
#         email = event['sender_email']
#         created = event['created']

#         # Send the chat message to the WebSocket
#         await self.send(text_data=json.dumps({
#             'type': 'chat_message',
#             'message': message,
#             'room_id': room_id,
#             'sender_email': email,
#             'created': created,
#         }))

#     @sync_to_async
#     def create_message(self, room_id, message, email):
#         user = User.objects.get(email=email)
#         message = ChatMessage.objects.create(content=message, sender=user)
#         message.save()
#         return message






























# import json

# from asgiref.sync import sync_to_async
# from channels.generic.websocket import AsyncWebsocketConsumer

# from django.utils.timesince import timesince

# from accounts.models import AccountUser

# from .models import ChatRoom, Message



# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'chat_{self.room_name}'
#         self.user = self.scope['user']

#         # Join room group
#         await self.get_room()
#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#         await self.accept()

#         # Inform user
#         if self.user.is_staff:
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     'type': 'users_update'
#                 }
#             )
    
    
#     async def disconnect(self, close_code):
#         # Leave room
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#         if not self.user.is_staff:
#             await self.set_room_closed()


#     async def receive(self, text_data):
#         # Receive message from WebSocket (front end)
#         text_data_json = json.loads(text_data)
#         type = text_data_json['type']
#         message = text_data_json['message']
#         name = text_data_json['name']
#         agent = text_data_json.get('agent', '')

#         print('Receive:', type)

#         if type == 'message':
#             new_message = await self.create_message(name, message, agent)

#             # Send message to group / room
#             await self.channel_layer.group_send(
#                 self.room_group_name, {
#                     'type': 'chat_message',
#                     'message': message,
#                     'name': name,
#                     'agent': agent,
                   
#                     'created_at': timesince(new_message.created_at),
#                 }
#             )
#         elif type == 'update':
#             print('is update')
#             # Send update to the room
#             await self.channel_layer.group_send(
#                 self.room_group_name, {
#                     'type': 'writing_active',
#                     'message': message,
#                     'name': name,
#                     'agent': agent,
                    
#                 }
#             )

    
#     async def chat_message(self, event):
#         # Send message to WebSocket (front end)
#         await self.send(text_data=json.dumps({
#             'type': event['type'],
#             'message': event['message'],
#             'name': event['name'],
#             'agent': event['agent'],
#             'initials': event['initials'],
#             'created_at': event['created_at'],
#         }))

    
#     async def writing_active(self, event):
#         # Send writing is active to room
#         await self.send(text_data=json.dumps({
#             'type': event['type'],
#             'message': event['message'],
#             'name': event['name'],
#             'agent': event['agent'],
#             'initials': event['initials'],
#         }))
    

#     async def users_update(self, event):
#         # Send information to the web socket (front end)
#         await self.send(text_data=json.dumps({
#             'type': 'users_update'
#         }))

    
#     @sync_to_async
#     def get_room(self):
#         self.room = ChatRoom.objects.get(uuid=self.room_name)

    
#     @sync_to_async
#     def set_room_closed(self):
#         self.room = ChatRoom.objects.get(uuid=self.room_name)
#         self.room.status = ChatRoom.CLOSED
#         self.room.save()


#     @sync_to_async
#     def create_message(self, sent_by, message, agent):
#         message = Message.objects.create(body=message, sent_by=sent_by)

#         if agent:
#             message.created_by = AccountUser.objects.get(pk=agent)
#             message.save()
        
#         self.room.messages.add(message)

#         return message
    


# # chat/consumers.py
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import ChatMessage
# from accounts.models import AccountUser
# from channels.db import database_sync_to_async
# import json

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope['user']
        
#         if self.user.is_authenticated:
#             await self.channel_layer.group_add(
#                 f'user_{self.user.id}',
#                 self.channel_name
#             )

#             await self.accept()
#         else:
#             await self.close()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             f'user_{self.user.id}',
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']
        
#         sender = self.user
#         admin_users = AccountUser.objects.filter(is_admin=True)
#         for admin in admin_users:
#             await self.save_message(sender, admin, message)

#     @database_sync_to_async
#     def save_message(self, sender, receiver, message):
#         ChatMessage.objects.create(
#             sender=sender,
#             receiver=receiver,
#             message=message,
#         )

#     async def chat_message(self, event):
#         message = event['message']
        
#         await self.send(text_data=json.dumps({
#             'message': message,
#         }))