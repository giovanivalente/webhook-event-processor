import logging
from uuid import UUID

from realmate_challenge.shared.exception import RealmateAPIError
from realmate_challenge.webhook_api.contracts.repositories.conversation_repository_contract import (
    ConversationRepositoryContract,
)
from realmate_challenge.webhook_api.dtos.webhook_dto import WebhookInputDTO
from realmate_challenge.webhook_api.entities.conversation_entity import ConversationEntity
from realmate_challenge.webhook_api.mapper import webhook_dto_to_open_conversation_entity

logger = logging.getLogger(__name__)


class CreateConversation:
    def __init__(self, conversation_repository: ConversationRepositoryContract):
        self._conversation_repository = conversation_repository

    def create_new_conversation(self, webhook_dto: WebhookInputDTO) -> ConversationEntity:
        conversation = webhook_dto_to_open_conversation_entity(webhook_dto)

        self._validate_conversation(conversation_id=conversation.id)

        created_conversation = self._conversation_repository.create_conversation(conversation)

        return created_conversation

    def _validate_conversation(self, conversation_id: UUID) -> None:
        conversation_already_exists = self._conversation_repository.get_conversation_by_id(
            conversation_id, raise_exception=False
        )

        if conversation_already_exists:
            logger.warning(f"Conversation with ID '{conversation_id}' already exists.")
            raise RealmateAPIError(detail='The conversation with the given ID already exists.')
