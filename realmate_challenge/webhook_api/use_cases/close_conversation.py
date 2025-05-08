import logging

from realmate_challenge.shared.exception import RealmateAPIError
from realmate_challenge.webhook_api.contracts.repositories.conversation_repository_contract import (
    ConversationRepositoryContract,
)
from realmate_challenge.webhook_api.dtos.webhook_dto import WebhookInputDTO
from realmate_challenge.webhook_api.entities.conversation_entity import ConversationEntity
from realmate_challenge.webhook_api.entities.enuns import ConversationStatus

logger = logging.getLogger(__name__)


class CloseConversation:
    def __init__(self, conversation_repository: ConversationRepositoryContract):
        self._conversation_repository = conversation_repository

    def close(self, webhook_dto: WebhookInputDTO) -> ConversationEntity:
        conversation = self._conversation_repository.get_conversation_by_id(webhook_dto.data.get('id'))

        self._validate_conversation(conversation)
        closed_conversation = self._conversation_repository.update_conversation(
            conversation=conversation, status=ConversationStatus.CLOSED.value
        )

        return closed_conversation

    def _validate_conversation(self, conversation: ConversationEntity) -> None:
        if conversation.status == ConversationStatus.CLOSED:
            logger.warning(f"Conversation with ID '{conversation.id}' is already closed.")
            raise RealmateAPIError(detail='A conversation with the given ID is already closed.')
