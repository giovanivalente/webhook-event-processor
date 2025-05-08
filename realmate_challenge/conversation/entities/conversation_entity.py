from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from rest_framework.exceptions import ValidationError, APIException

from realmate_challenge.conversation.entities.enuns import ConversationStatus


@dataclass
class ConversationEntity:
    id: UUID
    status: ConversationStatus
    external_timestamp: datetime
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def status_must_be_open(self):
        if self.status == ConversationStatus.CLOSED:
            raise APIException('This conversation is closed.')
