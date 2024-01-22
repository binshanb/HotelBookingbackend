# import os
# import django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booking_project.settings')
# django.setup()

# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from django.core.asgi import get_asgi_application

# django_asgi_application = get_asgi_application

# from chat import routing as routingchat


# application = ProtocolTypeRouter(
#     {
#         "http": get_asgi_application(),
#         'websocket': AuthMiddlewareStack(URLRouter(routingchat.websocket_urlpatterns),

#     }
# )


import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booking_project.settings')
django.setup()

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from chat import routing



django_asgi_app = get_asgi_application()



application = ProtocolTypeRouter(
    {
        "http" : django_asgi_app, 
        "websocket" : AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns
            )    
        )
    }
)

























# import os
# import django

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booking_project.settings')
# django.setup()

# from django.core.asgi import get_asgi_application
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from chat import routing



# django_asgi_app = get_asgi_application()



# application = ProtocolTypeRouter(
#     {
#         "http" : django_asgi_app, 
#         "websocket" : AuthMiddlewareStack(
#             URLRouter(
#                 routing.websocket_urlpatterns
#             )    
#         )
#     }
# )
















































