from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import CartAPIView, CartItemViewSet

app_name = 'carts'
urlpatterns = [
    path('', CartAPIView.as_view(), name='cart-detail')
]

router = DefaultRouter()
router.register('items', CartItemViewSet, basename='cart_items')
urlpatterns += router.urls
