from uuid import uuid4

from django.db import models

from realmate_challenge.webhook_api.entities.enuns import MessageDirection
from realmate_challenge.webhook_api.models.conversation import Conversation


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    direction = models.CharField(max_length=8, choices=MessageDirection.choices())
    external_timestamp = models.DateTimeField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Message - {self.id}'

    class Meta:
        db_table = 'message'
