# accounts/serializers.py
from djoser.serializers import UserCreatePasswordRetypeSerializer as BaseCreate
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class CustomUserCreateSerializer(BaseCreate):
    """
    Ensures 'username' is provided for create_user(), optionally
    auto-generated from the email if absent.
    """
    def validate(self, attrs):
        # Auto-generate username from email prefix if client didn't send one
        if not attrs.get('username'):
            attrs['username'] = attrs['email'].split('@')[0]
        return super().validate(attrs)

    class Meta(BaseCreate.Meta):
        model = User
        fields = ['id', 'email', 'password']
        read_only_fields = ['id']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id', 'email', 'username']