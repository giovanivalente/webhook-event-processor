from uuid import uuid4

from django.db import models

from realmate_challenge.conversation.entities.conversation import ConversationEntity
from realmate_challenge.conversation.entities.enuns import ConversationStatus


class Conversation(models.Model, ConversationEntity):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    status = models.CharField(max_length=6, choices=ConversationStatus.choices(), default=ConversationStatus.OPEN.value)
    external_timestamp = models.DateTimeField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation - {self.id} - ({self.status})"

    class Meta:
        db_table = 'conversation'
