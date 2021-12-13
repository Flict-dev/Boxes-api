from django.db import models
from items.models import Item
from users.models import User


class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='продукт')
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, verbose_name='корзина', related_name='cart_items')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='цена')
    quantity = models.PositiveIntegerField(verbose_name='кол-во товаров')

    class Meta:
        verbose_name = 'cart_item'
        verbose_name_plural = 'cart_items'
        unique_together = ('item', 'cart')

    def __str__(self):
        return f'cart item - {self.pk}'


class Cart(models.Model):
    items = models.ManyToManyField(Item, verbose_name='продуткы', related_name='carts', through=CartItem)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='владелец')

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'

    def __str__(self):
        return f'Корзина пользователя - {self.user.username} - {self.pk}'
