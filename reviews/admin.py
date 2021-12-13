from django.contrib import admin

from .models import Reviews


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'text',
        'created_at',
        'published_at',
        'status',
    )
    list_filter = ('author', 'created_at', 'published_at')