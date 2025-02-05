from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from openai import OpenAI
from .base import AIProvider


# class OpenAIProvider(AIProvider):
#     def validate_config(self):
#         if not hasattr(settings, "OPENAI_API_KEY"):
#             raise ImproperlyConfigured("OPENAI_API_KEY missing in settings")
#         return {
#             "api_key": settings.OPENAI_API_KEY,
#             "default_model": getattr(settings, "OPENAI_DEFAULT_MODEL", "gpt-4"),
#         }

#     def create_chat_completion(self, messages, **kwargs):
#         client = OpenAI(api_key=self.config["api_key"])
#         response = client.chat.completions.create(
#             model=kwargs.get("model", self.config["default_model"]),
#             messages=messages,
#             **kwargs
#         )
#         return {
#             "content": response.choices[0].message.content,
#             "tokens": response.usage.total_tokens,
#             "metadata": {
#                 "model": response.model,
#                 "finish_reason": response.choices[0].finish_reason,
#             },
#         }


class OpenAIProvider(AIProvider):
    def validate_config(self):
        """
        Validates and returns the configuration for the OpenAI provider.
        Raises ImproperlyConfigured if any required settings are missing.
        settings.py:
        OPENAI_CONFIG = {
            "api_key": "sk-1234567890", # REQUIRED
            "model": "gpt-4", # REQUIRED
            "role": {"role": "developer", "content": "You are a helpful assistant."}, # OPTIONAL
        }
        """
        api_key = getattr(settings, "OPENAI_API_KEY", None)
        if not api_key:
            raise ImproperlyConfigured("OPENAI_API_KEY is missing in settings")

        openai_model = getattr(settings, "OPENAI_MODEL", None)
        if not openai_model:
            raise ImproperlyConfigured("OPENAI_MODEL is missing in settings")

        openai_role = getattr(
            settings, "OPENAI_DEFAULT_ROLE", None
        )  # EXAMPLE: {"role": "developer", "content": "You are a helpful assistant."}

        return {
            "api_key": api_key,
            "model": openai_model,
            "role": openai_role,
        }

    def create_chat_completion(self, messages, **kwargs):
        """
        Creates a chat completion using the OpenAI API.

        Parameters:
            messages (list): A list of message objects to be sent to the API.
            **kwargs: Additional keyword arguments for the API call (e.g., model).

        Returns:
            dict: A dictionary containing the generated content, token usage, and metadata.

        Raises:
            Exception: Propagates any exceptions raised by the OpenAI API.
        """
        client = OpenAI(api_key=self.config["api_key"])
        model = kwargs.get("model", self.config["model"])

        if self.config["role"]:
            # append the role to the first index of the messages list
            messages.insert(0, self.config["role"])

        try:
            response = client.chat.completions.create(
                model=model, messages=messages, **kwargs
            )
        except Exception as e:
            # Optional: Log the exception details here
            raise e

        return {
            "content": response.choices[0].message.content,
            "tokens": response.usage.total_tokens,
            "metadata": {
                "model": response.model,
                "finish_reason": response.choices[0].finish_reason,
            },
        }
