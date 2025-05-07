from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from realmate_challenge.conversation.entities.enuns import ConversationStatus


@dataclass
class ConversationEntity:
    id: UUID
    status: ConversationStatus
    external_timestamp: datetime
    created_at: datetime | None = None
    updated_at: datetime | None = None
