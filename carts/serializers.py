from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from carts.models import Cart, CartItem
from items.models import Item
from items.serializers import ItemSerializer


class CartItemSerializer(ModelSerializer):
    total_price = serializers.SerializerMethodField('_get_total_price')
    item = ItemSerializer(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = CartItem
        fields = ('id', 'item', 'item_id', 'price', 'quantity', 'total_price')

    def _get_total_price(self, cart_item):
        return cart_item.price * int(cart_item.quantity)

    def create(self, validated_data):
        request = self.context.get('request')
        item = Item.objects.get(id=request.data['item'])
        cart = request.user.current_cart
        cart_item = CartItem(
            item=item,
            price=item.price,
            cart_id=cart.id,
            item_id=item.id,
            quantity=request.data['quantity'],
        )
        cart_item.save()
        cart.items.add(item)
        cart.save()
        return cart_item


class CartSerializer(ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)
    total_cost = serializers.SerializerMethodField('_get_total_cost')

    class Meta:
        model = Cart
        fields = ('id', 'cart_items', 'total_cost')

    def _get_total_cost(self, cart):
        cart_items = CartItemSerializer(cart.cart_items, many=True)
        total_cost = 0
        for item in range(cart.cart_items.count()):
            total_cost += cart_items.data[item]['total_price']
        return total_cost
