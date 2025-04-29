from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import  UserProfileSerializer

User = get_user_model()

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # Retrieve the authenticated user

    def list(self, request, *args, **kwargs):
        """ Restrict listing, return only the current user's profile. """
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

