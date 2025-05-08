from uuid import UUID

from rest_framework.exceptions import APIException

from realmate_challenge.webhook_api.contracts.repositories.conversation_repository_contract import (
    ConversationRepositoryContract,
)
from realmate_challenge.webhook_api.dtos.webhook_dto import WebhookInputDTO
from realmate_challenge.webhook_api.entities.conversation_entity import ConversationEntity
from realmate_challenge.webhook_api.entities.enuns import ConversationStatus


class CreateConversation:
    def __init__(self, conversation_repository: ConversationRepositoryContract):
        self._conversation_repository = conversation_repository

    def create(self, webhook_dto: WebhookInputDTO) -> ConversationEntity:
        conversation = ConversationEntity(
            id=webhook_dto.data.get('id'), status=ConversationStatus.OPEN, external_timestamp=webhook_dto.timestamp
        )

        self._validate_conversation(conversation_id=conversation.id)

        created_conversation = self._conversation_repository.create_conversation(conversation)

        return created_conversation

    def _validate_conversation(self, conversation_id: UUID) -> None:
        conversation_already_exists = self._conversation_repository.get_conversation_by_id(
            conversation_id, raise_exception=False
        )

        if conversation_already_exists:
            # TODO: refact
            # TODO: add log
            raise APIException(detail='Conversation already exist')
