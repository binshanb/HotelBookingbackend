import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booking_project.settings')
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

django_asgi_application = get_asgi_application

from chat import routing as routingchat


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        'websocket': URLRouter(routingchat.websocket_urlpatterns),

    }
)















# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from  chat.routing import websocket_urlpatterns

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booking_project.settings')

# application = ProtocolTypeRouter({
#     'http': get_asgi_application(),
#     'websocket': AuthMiddlewareStack(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     ),
# })


















# import os
# import django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booking_project.settings')
# django.setup()

# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# django_asgi_application = get_asgi_application

# from chat import routing as routingchat


# application = ProtocolTypeRouter(
#     {
#         "http": get_asgi_application(),
#         'websocket': URLRouter(routingchat.websocket_urlpatterns),

#     }
# )




















# import os
# import django

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booking_project.settings')
# django.setup()

# from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack
# from .channelsmiddleware import JwtAuthMiddleware
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter,URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator

# from chat import routing





# django_asgi_application = get_asgi_application()

# application = ProtocolTypeRouter(
#     {
#         'http': django_asgi_application,
#         'websocket': JwtAuthMiddleware(URLRouter(routing.websocket_urlpatterns)
#         )
#     }
# )




































# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator
# from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack
# from chat.routing import websocket_urlpatterns as accounts_websocket_urlpatterns
# # from post.routing import websocket_urlpatterns as post_websocket_urlpatterns

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booking_project.settings')
# django_asgi_application = get_asgi_application()

# application = ProtocolTypeRouter({
#     "http": django_asgi_application,
#     "websocket": AllowedHostsOriginValidator(
#         JWTAuthMiddlewareStack(
#              URLRouter(
#                  accounts_websocket_urlpatterns
#              )
#         )
#     ),
# })
# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from chat import routing

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "booking_project.settings")

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             routing.websocket_urlpatterns
#         )
#     ),
# })
