from django.db import models
from django.conf import settings
from django.utils import timezone


class SoftDelete(models.Model):
    """
    Abstract base class for soft deletion.
    Adds a `deleted_at` field to track when an instance is soft-deleted.
    """

    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        abstract = True  # Marks this as an abstract base class

    def soft_delete(self):
        """Soft delete the instance by setting `deleted_at` to the current time."""
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def restore(self):
        """Restore the instance by setting `deleted_at` to `None`."""
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])

    @property
    def is_deleted(self):
        """Check if the instance is soft-deleted."""
        return self.deleted_at is not None


class Conversation(SoftDelete, models.Model):
    """Model to group messages into conversations."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="conversations",
    )
    title = models.CharField(max_length=255, blank=True)  # Auto-generated title
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(
        blank=True, null=True, db_index=True
    )  # Tracks last message time
    metadata = models.JSONField(
        default=dict, blank=True
    )  # Store model info, API config, etc.

    class Meta:
        ordering = ["-last_activity"]
        indexes = [
            models.Index(fields=["user", "last_activity"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Ensure title is set using creation datetime format."""
        if not self.title:  # Set title only if it's empty
            self.title = f"New Chat - {timezone.localtime(self.created_at).strftime('%Y-%m-%d %H:%M:%S')}"
        if not self.pk:  # Initialize last_activity with creation time
            self.last_activity = self.created_at
        super().save(*args, **kwargs)


class ChatMessage(SoftDelete, models.Model):
    """Stores chatbot conversations with users."""

    class RoleChoices(models.TextChoices):
        SYSTEM = "system", "System"
        USER = "user", "User"
        ASSISTANT = "assistant", "Assistant"

    class StatusChoices(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        ERROR = "error", "Error"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_messages",
    )
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    role = models.CharField(max_length=9, choices=RoleChoices.choices, db_index=True)
    content = models.TextField()
    tokens = models.PositiveIntegerField(default=0)
    metadata = models.JSONField(
        default=dict, blank=True
    )  # Store model params, API response, etc.
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        db_index=True,
    )  # Status tracking for async responses

    class Meta:
        ordering = ["timestamp"]
        indexes = [
            models.Index(fields=["user", "timestamp"]),
            models.Index(fields=["conversation", "timestamp"]),
            models.Index(fields=["status"]),
            models.Index(fields=["deleted_at"]),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.role} - {self.timestamp}"

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # After saving, update the conversation's last_activity
        if self.conversation:
            self.conversation.last_activity = self.timestamp
            self.conversation.save(update_fields=["last_activity"])
