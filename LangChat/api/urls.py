
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatRoomViewSet, ChatMessageViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r'rooms', ChatRoomViewSet,basename='rooms')
router.register(r'messages', ChatMessageViewSet,basename='messages')
router.register(r'notifications', NotificationViewSet,basename='notifications')

urlpatterns = [
    path('', include(router.urls)),
]
