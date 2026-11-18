from django.contrib import admin
from .models import ChannelStat, ContentItem

@admin.register(ChannelStat)
class ChannelStatAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscriber_count', 'video_count', 'view_count', 'recorded_at']
    list_filter = ['recorded_at']
    search_fields = ['user__username', 'user__channel_name']

@admin.register(ContentItem)
class ContentItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'niche', 'target_date', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'user__username', 'description']
