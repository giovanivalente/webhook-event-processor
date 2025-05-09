import logging
from uuid import UUID

from realmate_challenge.shared.parse import parse_uuid
from realmate_challenge.webhook_api.contracts.repositories.conversation_repository_contract import (
    ConversationRepositoryContract,
)
from realmate_challenge.webhook_api.entities.conversation_entity import ConversationEntity

logger = logging.getLogger(__name__)


class ConversationDetail:

    def __init__(self, conversation_repository: ConversationRepositoryContract):
        self._conversation_repository = conversation_repository

    def get_conversation_by_id(self, conversation_id: str | UUID) -> ConversationEntity:
        if not isinstance(conversation_id, UUID):
            conversation_id = parse_uuid(conversation_id)

        conversation = self._conversation_repository.get_conversation_by_id(conversation_id)

        return conversation
