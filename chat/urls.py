# urls.py

from django.urls import path
from .views import ChatListCreateAPIView

urlpatterns = [
    path('chat-messages/', ChatListCreateAPIView.as_view(), name='chat-list-create'),  # Maps to POST and GET methods
    path('chat-messages/<int:chat_id>/', ChatListCreateAPIView.as_view(), name='chat-detail'),  # Maps to PUT method
    
]



























# from django.urls import path
# from .views import ChatRoomView, MessagesView

# urlpatterns = [
# 	path('chats', ChatRoomView.as_view(), name='chatRoom'),
# 	path('chats/<str:roomId>/messages', MessagesView.as_view(), name='messageList'),
# 	path('users/<int:userId>/chats', ChatRoomView.as_view(), name='chatRoomList'),
# ]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('api/user-chat/', views.UserChatView.as_view(), name='user-chat'),
#     path('api/admin-chat/', views.AdminChatView.as_view(), name='admin-chat'),
   
# ]


# from django.urls import path
# from .views import ExistingMessagesView

# urlpatterns = [
#     path('<int:appointment_id>/', ExistingMessagesView.as_view(), name='existing_messages'),
# ]


















# from django.urls import path
# from . import views

# urlpatterns = [
#     # URLs for user chat
#     path('messages/', views.UserChatView.as_view(), name='user_chat'),

#     # URLs for admin chat
#     path('admin/messages/', views.AdminChatView.as_view(), name='admin_chat'),
# ]













# from django.urls import path
# from .views import *

# urlpatterns = [
#     path('create-room/<int:pk>/', CreateChatRoom.as_view()),
#     path('chat-room/<int:pk>/', RoomMessagesView.as_view()),
#     path('chatrooms/', ChatRoomListView.as_view()),
#     path('seen/<int:pk>/', MesageSeenView.as_view()),

# ]



















# from django.urls import path
# from .views import ChatMessageListCreateAPIView,ChatMessageDetailAPIView

# urlpatterns = [
#     path('messages/', ChatMessageListCreateAPIView.as_view(), name='chat-message-list'),
#     path('messages/</', ChatMessageDetailAPIView.as_view(), name='chat-message-detail'),

# ]

















# from django.urls import path
# from . import views



# urlpatterns = [


#     # path('create_message/', views.MessageCreateView.as_view(), name='create-message'),
#     # path('messages/', views.MessageListView.as_view(), name='message-list'),
#     # path('create_chatroom/', views.ChatRoomCreateView.as_view(), name='create-chatroom'),
#     # path('chatrooms/', views.ChatRoomListView.as_view(), name='chatroom-list'),
# ]