from dataclasses import dataclass
from uuid import UUID
from xmlrpc.client import DateTime

from realmate_challenge.conversation.entities.enuns import ConversationStatus


@dataclass
class ConversationEntity:
    id: UUID
    status: ConversationStatus
    external_timestamp: DateTime
    created_at: DateTime
    updated_at: DateTime
