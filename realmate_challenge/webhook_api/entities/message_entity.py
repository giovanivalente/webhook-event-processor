from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from realmate_challenge.webhook_api.entities.conversation_entity import ConversationEntity
from realmate_challenge.webhook_api.entities.enuns import MessageDirection


@dataclass
class MessageEntity:
    id: UUID
    conversation: ConversationEntity
    content: str
    direction: MessageDirection
    external_timestamp: datetime
    created_at: datetime | None = None
    updated_at: datetime | None = None
