import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat import routing as routingchat

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booking_project.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        routingchat.websocket_urlpatterns
)
})




































