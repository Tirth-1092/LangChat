from rest_framework import serializers
from .models import ChatRoom, ChatMessage, Notification

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'created_at']


# class ChatMessageSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField(read_only=True)  # Display username
#     class Meta:
#         model = ChatMessage
#         fields = ['id', 'room', 'user', 'content', 'timestamp']

class ChatMessageSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'room', 'user', 'content', 'translation', 'timestamp']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'is_read', 'created_at']
