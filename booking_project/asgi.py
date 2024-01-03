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




































