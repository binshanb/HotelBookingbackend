from django.urls import path
from . import views
from .views import Last50MessagesView,ProviderChatRoomsView,UnseenMessagesCountView,MarkMessagesAsSeenView,TotalMessageCountView

urlpatterns = [
    path('chat-rooms/', views.CreateRoomView.as_view(), name='room-list'),
    path('messages/', views.MessageList.as_view(), name='message-list'),
    path('last-50-messages/<str:room_name>/', Last50MessagesView.as_view(), name='last-50-messages'),
    path('provider-chat-rooms/<int:provider_id>/', ProviderChatRoomsView.as_view(), name='provider-chat-rooms'),
    path('unseen-messages-count/<int:room_id>/', UnseenMessagesCountView.as_view(), name='unseen_messages_count'),
    path('mark-messages-as-seen/<int:room_id>/', MarkMessagesAsSeenView.as_view(), name='mark_messages_as_seen'),
    path('total-message-count/<int:provider_id>/', TotalMessageCountView.as_view(), name='total_message_count'),
]



















# from django.urls import path
# from . import views
# from .views import Last50MessagesView,ProviderChatRoomsView,UnseenMessagesCountView,MarkMessagesAsSeenView,TotalMessageCountView

# urlpatterns = [
#     path('chat-rooms/', views.CreateChatRoomView.as_view(), name='room-list'),
#     path('messages/', views.MessageList.as_view(), name='message-list'),
#     path('last-50-messages/<str:chatroom_name>/', Last50MessagesView.as_view(), name='last-50-messages'),
#     path('provider-chat-rooms/<int:provider_id>/', ProviderChatRoomsView.as_view(), name='provider-chat-rooms'),
#     path('unseen-messages-count/<int:chatroom_id>/', UnseenMessagesCountView.as_view(), name='unseen_messages_count'),
#     path('mark-messages-as-seen/<int:chatroom_id>/', MarkMessagesAsSeenView.as_view(), name='mark_messages_as_seen'),
#     path('total-message-count/<int:provider_id>/', TotalMessageCountView.as_view(), name='total_message_count'),
# ]













































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