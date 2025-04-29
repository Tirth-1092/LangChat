# api/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# class ChatMessage(models.Model):
#     room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
#     user = models.ForeignKey(User, related_name='chat_messages', on_delete=models.CASCADE)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['timestamp']

#     def __str__(self):
#         return f"{self.user.username}@{self.room.name} [{self.timestamp}]"

class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='chat_messages', on_delete=models.CASCADE)
    content = models.TextField()  # original
    translation = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.user.username}@{self.room.name} [{self.timestamp}]"

class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.CharField(max_length=512)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{'✓' if self.is_read else '✗'} {self.user.username}: {self.message[:50]}"
