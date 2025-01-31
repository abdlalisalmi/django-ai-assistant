from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from ..models import Conversation, ChatMessage


class ChatMessageModelTests(TestCase):
    def setUp(self):
        """Create a user and conversation for the tests."""
        self.user = get_user_model().objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.conversation = Conversation.objects.create(user=self.user)

    def test_create_chat_message(self):
        """Test creating a chat message."""
        message = ChatMessage.objects.create(
            user=self.user,
            conversation=self.conversation,
            role=ChatMessage.RoleChoices.USER,
            content="Hello",
        )
        self.assertEqual(message.content, "Hello")
        self.assertEqual(message.user, self.user)
        self.assertEqual(message.conversation, self.conversation)
        self.assertEqual(message.role, ChatMessage.RoleChoices.USER)

    def test_chat_message_status(self):
        """Test the status field of ChatMessage."""
        message = ChatMessage.objects.create(
            user=self.user,
            conversation=self.conversation,
            role=ChatMessage.RoleChoices.USER,
            content="Hello",
            status=ChatMessage.StatusChoices.PENDING,
        )
        self.assertEqual(message.status, ChatMessage.StatusChoices.PENDING)

        message.status = ChatMessage.StatusChoices.COMPLETED
        message.save()

        message.refresh_from_db()
        self.assertEqual(message.status, ChatMessage.StatusChoices.COMPLETED)

    def test_chat_message_tokens_field(self):
        """Test the tokens field for chat messages."""
        message = ChatMessage.objects.create(
            user=self.user,
            conversation=self.conversation,
            role=ChatMessage.RoleChoices.USER,
            content="Hello",
            tokens=50,
        )
        self.assertEqual(message.tokens, 50)

    def test_soft_delete_chat_message(self):
        """Test soft deletion for ChatMessage."""
        message = ChatMessage.objects.create(
            user=self.user,
            conversation=self.conversation,
            role=ChatMessage.RoleChoices.USER,
            content="Hello",
        )
        self.assertIsNone(message.deleted_at)

        message.soft_delete()
        self.assertIsNotNone(message.deleted_at)

        message.restore()
        self.assertIsNone(message.deleted_at)

    def test_is_deleted_property_on_chat_message(self):
        """Test the `is_deleted` property for ChatMessage."""
        message = ChatMessage.objects.create(
            user=self.user,
            conversation=self.conversation,
            role=ChatMessage.RoleChoices.USER,
            content="Hello",
        )
        self.assertFalse(message.is_deleted)

        message.soft_delete()
        self.assertTrue(message.is_deleted)

        message.restore()
        self.assertFalse(message.is_deleted)
