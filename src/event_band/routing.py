from django.urls import path
from event_band import consumers

websocket_urlpatterns = [
    path('ws/notifications/', consumers.NotificationConsumer.as_asgi()),
]
