from django.db import models

class LLM(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content

class ChatHistory(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Chat at {self.timestamp}"