from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/chat-messages/', consumers.ChatConsumer.as_asgi()),
]















# from django.urls import re_path
# from django.urls import re_path
# from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/chat/(?P<room_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
# ]

























# from django.urls import path
# from . import consumers

# websocket_urlpatterns = [
# 	path('ws/users/chat/', consumers.ChatConsumer.as_asgi()),
# ]










# from django.urls import re_path
# from .consumers import ChatConsumer


    
# websocket_urlpatterns = [
#     re_path(r'ws/chat/$', ChatConsumer.as_asgi()),
# ]





















# from django.urls import re_path
# from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
# ]












# from django.urls import path

# from . import consumers

# websocket_urlpatterns = [
#     path('ws/chat/<int:room_id>/', consumers.ChatConsumer.as_asgi()),
# ]











# from django.urls import path

# from . import consumers


# websocket_urlpatterns = [
#     path('ws/chat/<int:user_id>/', consumers.ChatConsumer.as_asgi()),
# ]






















# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.urls import re_path
# from chat.consumers import ChatConsumer

# websocket_urlpatterns = [
#     re_path(r'chat/', ChatConsumer.as_asgi()),
# ]