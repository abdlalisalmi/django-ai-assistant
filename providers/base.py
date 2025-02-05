from abc import ABC, abstractmethod


class AIProvider(ABC):
    def __init__(self):
        self.config = self.validate_config()

    @abstractmethod
    def validate_config(self):
        """Validate required settings"""
        pass

    @abstractmethod
    def create_chat_completion(self, messages, **kwargs):
        """Create chat completion with provider API"""
        pass

    def format_messages(self, queryset):
        """Convert Message queryset to provider format"""
        return [{"role": msg.role, "content": msg.content} for msg in queryset]
