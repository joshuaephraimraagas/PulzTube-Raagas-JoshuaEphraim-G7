from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        CREATOR = "CREATOR", "Content Creator"
        ADMIN = "ADMIN", "Administrator"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CREATOR,
        help_text="Role determining user dashboard access and permissions."
    )

    # Unique email required by project rubric
    email = models.EmailField(
        unique=True,
        help_text="Required. Must be a valid and unique email address."
    )

    # Creator-specific attributes
    channel_name = models.CharField(
        max_length=150,
        blank=True,
        help_text="Name of your YouTube channel."
    )
    channel_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="YouTube Channel ID or @handle (used for YouTube Data API v3 stats)."
    )
    niche = models.CharField(
        max_length=100,
        blank=True,
        help_text="Primary content niche (e.g., Tech, Gaming, Education, Lifestyle)."
    )
    content_interests = models.TextField(
        blank=True,
        help_text="Content topics, formats, or goals you are focusing on."
    )
    contact_number = models.CharField(
        max_length=20,
        blank=True,
        help_text="Optional contact phone number."
    )
    profile_photo = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
        help_text="Upload an optional profile or avatar image."
    )

    @property
    def is_creator(self):
        return self.role == self.Role.CREATOR

    @property
    def is_admin_user(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def __str__(self):
        if self.channel_name:
            return f"{self.username} ({self.channel_name}) - {self.get_role_display()}"
        return f"{self.username} - {self.get_role_display()}"
