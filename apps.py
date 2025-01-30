from django.apps import AppConfig


class DjangoAiAssistantConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_ai_assistant"
    verbose_name = "Django AI Assistant"

    def ready(self):
        # Add signal handlers or other initialization code
        pass
