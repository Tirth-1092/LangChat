from django.urls import path, include
from .views import UserProfileViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename='user-profile')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/jwt/create/', TokenObtainPairView.as_view(), name='jwt-create'),
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('', include(router.urls)),  # ← This line adds your /profile route
]