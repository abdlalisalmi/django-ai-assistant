from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from ..models import Conversation, ChatMessage


class ConversationModelTests(TestCase):
    def setUp(self):
        """Create a user for the tests."""
        self.user = get_user_model().objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )

    def test_create_conversation(self):
        """Test creating a conversation."""
        conversation = Conversation.objects.create(user=self.user)
        self.assertEqual(conversation.user, self.user)
        self.assertIsNotNone(conversation.created_at)

    def test_auto_title_on_creation(self):
        """Test that a title is auto-generated if not provided."""
        conversation = Conversation.objects.create(user=self.user)
        self.assertTrue(conversation.title.startswith("New Chat - "))

    def test_last_activity_on_message(self):
        """Test that last_activity is updated when a new message is added."""
        conversation = Conversation.objects.create(user=self.user)
        message = ChatMessage.objects.create(
            user=self.user,
            conversation=conversation,
            role=ChatMessage.RoleChoices.USER,
            content="Hello",
        )
        conversation.refresh_from_db()  # Refresh to get updated values
        self.assertEqual(conversation.last_activity, message.timestamp)

    def test_soft_delete(self):
        """Test soft delete functionality."""
        conversation = Conversation.objects.create(
            user=self.user, title="Test Conversation"
        )
        self.assertIsNone(conversation.deleted_at)

        conversation.soft_delete()
        self.assertIsNotNone(conversation.deleted_at)

        conversation.restore()
        self.assertIsNone(conversation.deleted_at)
