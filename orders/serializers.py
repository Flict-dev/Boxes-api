from rest_framework import serializers

from carts.models import Cart
from carts.serializers import CartSerializer
from orders.models import Order
from users.serializers import UserSerializer


class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)
    total_cost = serializers.SerializerMethodField('_get_total_cost')
    delivery_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    recipient = UserSerializer(write_only=True, required=False)

    def _get_total_cost(self, order):
        cart = CartSerializer(order.cart)
        return cart.data['total_cost']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        try:
            cart = Cart.objects.get(user=user, order__isnull=True)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user)
        serializer = CartSerializer(cart)
        order = Order(
            recipient=user,
            cart=cart,
            address=request.data['address'],
            delivery_at=request.data['delivery_at'],
            total_cost=serializer.data['total_cost']
        )
        order.save()
        return order

    class Meta:
        model = Order
        fields = (
            'id',
            'cart',
            'status',
            'recipient',
            'total_cost',
            'address',
            'delivery_at',
            'created_at',
        )
