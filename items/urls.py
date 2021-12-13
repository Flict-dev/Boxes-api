from rest_framework.routers import DefaultRouter

from items.views import ItemViewSet

app_name = 'items'
router = DefaultRouter()
router.register('', ItemViewSet, basename='item')
urlpatterns = router.urls
