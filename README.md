# Django AI Assistant

**Django AI Assistant** is a reusable Django package that integrates AI-powered chatbot functionality into your Django projects. It supports multiple AI providers (OpenAI, etc.) and is designed to be easy to install, configure, and extend.

### Features

- [x] **Conversations Management**:
  - [x] **Multi-Conversations Support**: multiple simultaneous conversations between users and chatbots, ensuring a smooth and context-aware chat experience.
  - [x] **User-Centric Conversations**: Store and manage chat history for individual users.
  - [x] **Soft Deletion**: Conversations can be marked as deleted without removing them from the database.
- [x] **Chat Messages Management**:

  - [x] **Conversation-Specific Messages**: Message are linked to specific conversation and allow metadata storage per message.
  - [x] **Soft Deletion**: Messages can be marked as deleted without removing them from the database.

- [x] **Multi-AI Provider Support**: Easily switch between AI providers like OpenAI and DeepSeek.
- [x] **Token Tracking**: Track token usage for cost management and optimization.
- [x] **Extensible Architecture**: Add custom AI providers or extend functionality with ease.

- [x] **Caching**: Optimize performance with built-in caching for chat history.

- [ ] **Customizable API Integration**: Supports AI API options like OpenAI and DeepSeek for chatbot responses.
- [ ] **Timestamp and Status Tracking**: Tracks timestamps for messages and provides status tracking for asynchronous processes.
- [ ] **Admin Integration**: Ability to manage conversations and messages via the Django admin interface.

## Installation

### 1. Install the package

Make sure this app is added to the `INSTALLED_APPS` list in your Django project’s `settings.py` file.

```python
INSTALLED_APPS = [
    ...
    'django_ai_assistant',  # Add the app name here
    ...
]
```
