from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from sorl.thumbnail.admin import AdminImageMixin

from .models import User


@admin.register(User)
class UserAdmin(AdminImageMixin, BaseUserAdmin):
    model = User
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'image',
        'score',
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            'Персональная информация',
            {'fields': ('first_name', 'last_name', 'email', 'image', 'score')},
        ),
        (
            'Права доступа',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
