from django.urls import path
from rest_framework.routers import DefaultRouter

from reviews.views import ReviewViewSet

app_name = 'review'
router = DefaultRouter()
router.register('', ReviewViewSet, basename='reviews')
urlpatterns = router.urls
