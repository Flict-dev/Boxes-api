from django.urls import path
from rest_framework.authtoken import views

from users.views import (
    RegisterAPIView,
    CurrentUserViewSet,
)

urlpatterns = [
    path('auth/login/', views.obtain_auth_token, name='user-login'),
    path('auth/register/', RegisterAPIView.as_view(), name='user-register'),
    path('current/', CurrentUserViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'}
    ), name='user-current')
]