# views.py

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChatRoom, ChatMessage
from .serializer import ChatRoomSerializer, MessageSerializer,UnseenMessagesCountSerializer,MessageCountSerializer
from django.shortcuts import get_object_or_404
from accounts.models import AccountUser
from django.http import JsonResponse

class CreateRoomView(CreateAPIView):
    serializer_class = ChatRoomSerializer

    def create(self, request, *args, **kwargs):
        print(request,"reqqqqqqqq")
        # care_home_id = request.data.get('care_home_id')
        user_id = request.data.get('user_id')
        print(user_id,"userid")
        provider_id = request.data.get('provider_id')
        print(provider_id,"providerid")
        username=request.data.get('username')
        print(username,"username")

        # Construct a more unique room name using both care_home_id and user_id
        room_name = f"AccountUser_{provider_id}_{user_id}"
        print(room_name,"roomname")

        # Check if the room already exists
        existing_room = ChatRoom.objects.filter(name=room_name).first()
      
        if existing_room:
            print('alredy have ')
            return Response(ChatRoomSerializer(existing_room).data, status=status.HTTP_200_OK)
        
        try:
            provider = AccountUser.objects.get(id=provider_id)
        
        except AccountUser.DoesNotExist:
            return Response({"error": "Provider not found."}, status=status.HTTP_400_BAD_REQUEST)
        

        # Create room
        room = ChatRoom(name=room_name,provider=provider,username=username)
        room.save()
        print(room,"chatroom")

        serializer = ChatRoomSerializer(room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class MessageList(generics.ListCreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = MessageSerializer


class Last50MessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        room_name = self.kwargs['room_name']
        room = get_object_or_404(ChatRoom, name=room_name)
        return ChatMessage.objects.filter(room=room).order_by('timestamp')[:50]


class ProviderChatRoomsView(generics.ListAPIView):
    serializer_class = ChatRoomSerializer

    def get_queryset(self):
        provider_id = self.kwargs['provider_id']
        return ChatRoom.objects.filter(provider__id=provider_id)
    

class UnseenMessagesCountView(APIView):
    @staticmethod
    def get(request, room_id):
        room = get_object_or_404(ChatRoom, id=room_id)
        unseen_count = room.messages.filter(is_seen=False).count()

        serializer = UnseenMessagesCountSerializer({'unseen_count': unseen_count})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class MarkMessagesAsSeenView(generics.UpdateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = MessageSerializer

    def update(self, request, *args, **kwargs):
        room_id = kwargs.get('room_id')
        room = get_object_or_404(ChatRoom, id=room_id)
        messages = room.messages.filter(is_seen=False)
        
        # Mark messages as seen
        messages.update(is_seen=True)

        return Response({'success': True})
    

class TotalMessageCountView(generics.ListAPIView):
    serializer_class = MessageCountSerializer

    def get_queryset(self):
        provider_id = self.kwargs['provider_id']
        rooms = ChatRoom.objects.filter(provider__id=provider_id)
        total_message_count = ChatMessage.objects.filter(room__in=rooms,is_seen=False).count()

        return [{'provider_id': provider_id, 'total_message_count': total_message_count}]















































# # views.py

# from rest_framework import generics
# from rest_framework.views import APIView
# from rest_framework.generics import CreateAPIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import ChatRoom, Message
# from .serializer import ChatRoomSerializer, MessageSerializer,UnseenMessagesCountSerializer,MessageCountSerializer
# from django.shortcuts import get_object_or_404
# from accounts.models import AccountUser
# from django.http import JsonResponse

# class CreateChatRoomView(CreateAPIView):
#     serializer_class = ChatRoomSerializer

#     def create(self, request, *args, **kwargs):
#         user_id = request.data.get('user_id')
#         provider_id = request.data.get('provider_id')
#         username=request.data.get('username')
#         print(username)

#         # Construct a more unique room name using both care_home_id and user_id
#         chatroom_name = f"AccountUser_{user_id}"

#         # Check if the room already exists
#         existing_room = ChatRoom.objects.filter(name=chatroom_name).first()
#         if existing_room:
#             print('already have ')
#             return Response(ChatRoomSerializer(existing_room).data, status=status.HTTP_200_OK)
        
#         try:
#             provider = AccountUser.objects.get(id=provider_id)
#         except AccountUser.DoesNotExist:
#             return Response({"error": "Provider not found."}, status=status.HTTP_400_BAD_REQUEST)


#         # Create room
#         chatroom = ChatRoom(name=chatroom_name,provider=provider,username=username)
#         chatroom.save()

#         serializer = ChatRoomSerializer(chatroom)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# class MessageList(generics.ListCreateAPIView):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer


# class Last50MessagesView(generics.ListAPIView):
#     serializer_class = MessageSerializer

#     def get_queryset(self):
#         chatroom_name = self.kwargs['chatroom_name']
#         chatroom = get_object_or_404(ChatRoom, name=chatroom_name)
#         return Message.objects.filter(chatroom=chatroom).order_by('timestamp')[:50]


# class ProviderChatRoomsView(generics.ListAPIView):
    
#     serializer_class = ChatRoomSerializer

#     def get_queryset(self):
#         provider_id = self.kwargs['provider_id']
#         return ChatRoom.objects.filter(provider__id=provider_id)
    

# class UnseenMessagesCountView(APIView):
#     @staticmethod
#     def get(request, chatroom_id):
#         chatroom = get_object_or_404(ChatRoom, id=chatroom_id)
#         unseen_count = chatroom.messages.filter(is_seen=False).count()

#         serializer = UnseenMessagesCountSerializer({'unseen_count': unseen_count})
#         return Response(serializer.data, status=status.HTTP_200_OK)
    

# class MarkMessagesAsSeenView(generics.UpdateAPIView):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer

#     def update(self, request, *args, **kwargs):
#         chatroom_id = kwargs.get('room_id')
#         chatroom = get_object_or_404(ChatRoom, id=chatroom_id)
#         messages = chatroom.messages.filter(is_seen=False)
        
#         # Mark messages as seen
#         messages.update(is_seen=True)

#         return Response({'success': True})
    

# class TotalMessageCountView(generics.ListAPIView):
#     serializer_class = MessageCountSerializer

#     def get_queryset(self):
#         provider_id = self.kwargs['provider_id']
#         chatrooms = ChatRoom.objects.filter(provider__id=provider_id)
#         total_message_count = Message.objects.filter(room__in=chatrooms,is_seen=False).count()

#         return [{'provider_id': provider_id, 'total_message_count': total_message_count}]
















































# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.generics import ListAPIView
# from rest_framework.pagination import LimitOffsetPagination
# from .serializer import ChatRoomSerializer, ChatMessageSerializer
# from .models import ChatRoom, ChatMessage

# class ChatRoomView(APIView):
# 	def get(self, request, userId):
# 		chatRooms = ChatRoom.objects.filter(member=userId)
# 		serializer = ChatRoomSerializer(
# 			chatRooms, many=True, context={"request": request}
# 		)
# 		return Response(serializer.data, status=status.HTTP_200_OK)

# 	def post(self, request):
# 		serializer = ChatRoomSerializer(
# 			data=request.data, context={"request": request}
# 		)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data, status=status.HTTP_200_OK)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class MessagesView(ListAPIView):
# 	serializer_class = ChatMessageSerializer
# 	pagination_class = LimitOffsetPagination

# 	def get_queryset(self):
# 		roomId = self.kwargs['roomId']
# 		return ChatMessage.objects.\
# 			filter(chat__roomId=roomId).order_by('-timestamp')





# from rest_framework.generics import ListCreateAPIView
# from .models import ChatMessage
# from .serializer import ChatMessageSerializer
# from django.contrib.auth.models import User

# class UserChatView(ListCreateAPIView):
#     serializer_class = ChatMessageSerializer

#     def get_queryset(self):
#         user = self.request.user  # Get the current logged-in user
#         admin = User.objects.get(is_staff=True)  # Assuming there's an admin user

#         # Fetch messages between the current user and admin
#         return ChatMessage.objects.filter(sender=user, recipient=admin).order_by('timestamp')

#     def perform_create(self, serializer):
#         serializer.save(sender=self.request.user, recipient=User.objects.get(is_staff=True))

# class AdminChatView(ListCreateAPIView):
#     serializer_class = ChatMessageSerializer

#     def get_queryset(self):
#         user = self.request.user  # Get the current logged-in user
#         admin = User.objects.get(is_staff=True)  # Assuming there's an admin user

#         # Fetch messages between admin and the current user
#         return ChatMessage.objects.filter(sender=admin, recipient=user).order_by('timestamp')

#     def perform_create(self, serializer):
#         serializer.save(sender=User.objects.get(is_staff=True), recipient=self.request.user)























# # Create a new Django REST API view
# # chat/views.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import ChatMessage

# class ExistingMessagesView(APIView):
#     def get(self, request, appointment_id):
#         messages = ChatMessage.objects.filter(appointment_id=appointment_id).order_by('timestamp')
#         data = [
#             {
#                 'message': message.message,
#                 'sender' : message.sender.name,
#                 'sender_id': message.sender.id,
#                 'reciever' : message.receiver.name,
#                 'receiver_id': message.receiver.id,
#                 'timestamp' : message.timestamp            
#             } 
            
#             for message in messages
#         ]
#         return Response(data)
























# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import ChatMessage
# from .serializer import ChatMessageSerializer

# class UserChatView(APIView):
#     def get(self, request):
#         # Logic to fetch user chat messages
#         user = request.user  # Assuming user is authenticated
#         messages = ChatMessage.objects.filter(sender=user)
#         serializer = ChatMessageSerializer(messages, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         # Logic to send message in user chat
#         user = request.user  # Assuming user is authenticated
#         data = request.data
#         data['sender'] = user.id
#         serializer = ChatMessageSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Message sent successfully'}, status=201)
#         return Response(serializer.errors, status=400)


# class AdminChatView(APIView):
#     def get(self, request):
#         # Logic to fetch admin chat messages
#         admin = request.user  # Assuming admin is authenticated
#         messages = ChatMessage.objects.filter(receiver=admin)
#         serializer = ChatMessageSerializer(messages, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         # Logic to send message in admin chat
#         admin = request.user  # Assuming admin is authenticated
#         data = request.data
#         data['receiver'] = admin.id
#         serializer = ChatMessageSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Message sent successfully'}, status=201)
#         return Response(serializer.errors, status=400)

































# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework import permissions, status, generics
# from django.contrib.auth import get_user_model
# from rest_framework.response import Response
# from chat.models import ChatRoom, Message
# from . serializer import ChatRoomListSerializer, ChatRoomSerializer, MessageSerializer

# from django.db.models import Q
# User = get_user_model()

# # Create your views here.


# class CreateChatRoom(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = ChatRoomSerializer
 
#     def post(self, request, pk):
#         current_user = request.user
#         other_user = User.objects.get(pk=pk)

#         # Check if a chat room already exists between the users
#         existing_chat_rooms = ChatRoom.objects.filter(members=current_user).filter(members=other_user)
#         if existing_chat_rooms.exists():
#             serializer = ChatRoomSerializer(existing_chat_rooms.first())
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         # Create a new chat room
#         chat_room = ChatRoom()
#         chat_room.save()
#         chat_room.members.add(current_user, other_user)
        
#         serializer = ChatRoomSerializer(chat_room)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class RoomMessagesView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = MessageSerializer
 
#     def get(self, request, pk):
#         try:
#             room = ChatRoom.objects.get(pk=pk)
#             messages = Message.objects.filter(room=room)
#             serialized_messages = self.serializer_class(messages, many=True).data
#             return Response(serialized_messages, status=status.HTTP_200_OK)
#         except ChatRoom.DoesNotExist:
#             return Response("Room not found", status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


        
# class MesageSeenView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = MessageSerializer
 
#     def get(self, request, pk):
#         current_user = request.user
#         other_user = User.objects.get(pk=pk)
#         if ChatRoom.objects.filter(members=current_user).filter(members=other_user).exists():
#             chat_room = ChatRoom.objects.filter(members=current_user).filter(members=other_user).first()
#             messages_to_update = Message.objects.filter(Q(room=chat_room) & ~Q(sender=current_user))            
#             messages_to_update.update(is_seen=True)            
#             return Response({'sucess': 'Chat room found.'},status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Chat room not found.'}, status=status.HTTP_404_NOT_FOUND)
        

# class ChatRoomListView(generics.ListAPIView):
#     serializer_class = ChatRoomListSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return ChatRoom.objects.filter(members=user)
# views.py
# from rest_framework import generics
# from .models import ChatMessage
# from .serializer import ChatMessageSerializer
# from accounts.models import AccountUser 
# from rest_framework import status
# from rest_framework.response import Response

# class ChatMessageListCreateAPIView(generics.ListCreateAPIView):
#     queryset = ChatMessage.objects.all()
#     serializer_class = ChatMessageSerializer

#     def create(self, request, *args, **kwargs):
#         sender_user_id = request.data.get('sender')  # Get sender ID from request data
#         admin_instance = AccountUser.objects.get(is_admin=True)  # Fetch admin instance

#         # Check if the sender ID is provided and valid
#         if sender_user_id:
#             try:
#                 sender_user_instance = AccountUser.objects.get(id=sender_user_id)
#             except AccountUser.DoesNotExist:
#                 return Response({'error': 'Sender user does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
            
#             # Create a new ChatMessage instance
#             serializer = self.get_serializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save(sender=sender_user_instance, receiver=admin_instance)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({'error': 'Sender ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

# class ChatMessageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = ChatMessage.objects.all()
#     serializer_class = ChatMessageSerializer





















# # chat/views.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import ChatMessage

# class UserMessagesView(APIView):
#     def get(self, request, user_id):
#         messages = ChatMessage.objects.filter(receiver_id=user_id).order_by('timestamp')
#         data = [
#             {
#                 'message': message.message,
#                 'sender_id': message.sender.id,
#                 'timestamp': message.timestamp
#             } 
#             for message in messages
#         ]
#         return Response(data)

# class MessageCreateView(generics.CreateAPIView):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer

#     def perform_create(self, serializer):
#         serializer.save()

# class MessageListView(generics.ListAPIView):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer

# class ChatRoomCreateView(generics.CreateAPIView):
#     queryset = ChatRoom.objects.all()
#     serializer_class = ChatRoomSerializer

# class ChatRoomListView(generics.ListAPIView):
#     queryset = ChatRoom.objects.all()
#     serializer_class = ChatRoomSerializer


























# from rest_framework import generics
# from .models import Message
# from .serializer import MessageSerializer

# class MessageList(generics.ListCreateAPIView):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer
#     ordering = ('-timestamp',)


























# from rest_framework.views import APIView
# from rest_framework import permissions, status, generics
# from rest_framework.response import Response

# from django.db.models import Q
# from django.contrib.auth import get_user_model

# from .models import ChatRoom,Message
# from .serializer import *

# User = get_user_model()


# class SendChatView(generics.CreateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = MessageSerializer

#     def post(self, request, pk):
#         content = request.data.get('content')
#         if content:
#             # Assuming Message model has 'room_id' and 'content' fields
#             message = Message.objects.create(room_id=pk, content=content)
#             serializer = self.serializer_class(message)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response("Content cannot be empty", status=status.HTTP_400_BAD_REQUEST)


# class GetRoomMessagesView(generics.ListAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = MessageSerializer

#     def get_queryset(self):
#         chat_room_id = self.kwargs['pk']
#         return Message.objects.filter(room_id=chat_room_id)

#     def get(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serialized_data = self.serializer_class(queryset, many=True).data
#         return Response(serialized_data, status=status.HTTP_200_OK)


# class GetRoomsView(generics.ListAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = ChatRoomSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return ChatRoom.objects.filter(members=user)

#     def get(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serialized_data = self.serializer_class(queryset, many=True).data
#         return Response(serialized_data, status=status.HTTP_200_OK)
