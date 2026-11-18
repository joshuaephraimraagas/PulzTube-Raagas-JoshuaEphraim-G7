from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = [
        'username',
        'email',
        'channel_name',
        'role',
        'niche',
        'is_staff',
        'is_active',
        'date_joined',
    ]
    list_filter = ['role', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'channel_name', 'channel_id', 'niche']
    ordering = ['-date_joined']

    fieldsets = UserAdmin.fieldsets + (
        (
            'PulzTube Creator Details',
            {
                'fields': (
                    'role',
                    'channel_name',
                    'channel_id',
                    'niche',
                    'content_interests',
                    'contact_number',
                    'profile_photo',
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'PulzTube Creator Details',
            {
                'fields': (
                    'email',
                    'role',
                    'channel_name',
                    'channel_id',
                    'niche',
                    'contact_number',
                )
            },
        ),
    )
