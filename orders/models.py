from django.contrib.auth import get_user_model
from django.db import models

from carts.models import Cart


class Order(models.Model):
    class StatusChoices(models.TextChoices):
        CREATED = 'created'
        DELIVERED = 'delivered'
        PROCESSED = 'processed'
        CANCELLED = 'cancelled'

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    delivery_at = models.DateTimeField(verbose_name='Дата доставки', null=True)
    recipient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Получатель')
    address = models.CharField(max_length=60, verbose_name='Адрес')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина', related_name='order')
    status = models.CharField(choices=StatusChoices.choices, default=StatusChoices.CREATED, max_length=40, verbose_name='Статус')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая сумма')

    def __str__(self):
        return f'Заказ пользоветля - {self.recipient.username}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
