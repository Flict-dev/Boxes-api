from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'delivery_at',
        'recipient',
        'address',
        'cart',
        'status',
        'total_cost',
    )
    list_filter = ('created_at', 'delivery_at', 'recipient', 'cart')
    date_hierarchy = 'created_at'

