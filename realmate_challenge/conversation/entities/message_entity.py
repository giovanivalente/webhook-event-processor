from dataclasses import dataclass
from uuid import UUID
from xmlrpc.client import DateTime

from realmate_challenge.conversation.entities.conversation_entity import ConversationEntity
from realmate_challenge.conversation.entities.enuns import MessageDirection


@dataclass
class MessageEntity:
    id: UUID
    conversation: ConversationEntity
    content: str
    direction: MessageDirection
    external_timestamp: DateTime
    created_at: DateTime | None = None
    updated_at: DateTime | None = None
