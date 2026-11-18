from django.db import models
from django.conf import settings

class ChannelStat(models.Model):
    """
    Stores dated historical records of public YouTube channel statistics
    retrieved via the YouTube Data API v3 (Sprint 2 deliverable).
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="channel_stats"
    )
    subscriber_count = models.PositiveIntegerField(default=0)
    video_count = models.PositiveIntegerField(default=0)
    view_count = models.BigIntegerField(default=0)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f"{self.user.username} Stats @ {self.recorded_at.strftime('%Y-%m-%d %H:%M')}"


class ContentItem(models.Model):
    """
    Represents a video idea or planned upload in the creator's production pipeline.
    Implements the 7 production stages defined in the PulzTube proposal.
    """
    class Status(models.TextChoices):
        IDEA = "IDEA", "Idea"
        PLANNING = "PLANNING", "Planning"
        RECORDING = "RECORDING", "Recording"
        EDITING = "EDITING", "Editing"
        READY = "READY", "Ready"
        SCHEDULED = "SCHEDULED", "Scheduled"
        PUBLISHED = "PUBLISHED", "Published"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="content_items"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    niche = models.CharField(max_length=100, blank=True)
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.IDEA
    )
    target_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} [{self.get_status_display()}]"
