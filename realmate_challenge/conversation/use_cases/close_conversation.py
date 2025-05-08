from rest_framework.exceptions import APIException

from realmate_challenge.conversation.contracts.repositories.conversation_repository_contract import (
    ConversationRepositoryContract,
)
from realmate_challenge.conversation.dtos.webhook_dto import WebhookInputDTO
from realmate_challenge.conversation.entities.conversation_entity import ConversationEntity
from realmate_challenge.conversation.entities.enuns import ConversationStatus


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
            # TODO: refact
            # TODO: add log
            raise APIException(detail='Conversation already closed')
