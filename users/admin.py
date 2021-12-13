from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'password',
        'last_login',
        'is_superuser',
        'username',
        'email',
        'is_staff',
        'is_active',
        'date_joined',
        'middle_name',
        'phone',
        'address',
        'premium',
    )
    list_filter = (
        'last_login',
        'is_superuser',
        'is_staff',
        'is_active',
        'date_joined',
        'premium',
    )
    list_display_links = ('id', 'first_name')
    list_editable = ('premium',)
    raw_id_fields = ('groups', 'user_permissions')
