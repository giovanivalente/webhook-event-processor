from uuid import UUID

from rest_framework.exceptions import APIException

from realmate_challenge.conversation.contracts.repositories.conversation_repository_contract import (
    ConversationRepositoryContract,
)
from realmate_challenge.conversation.contracts.repositories.message_repository_contract import MessageRepositoryContract
from realmate_challenge.conversation.dtos.webhook_dto import WebhookInputDTO
from realmate_challenge.conversation.entities.conversation_entity import ConversationEntity
from realmate_challenge.conversation.entities.enuns import MessageDirection
from realmate_challenge.conversation.entities.message_entity import MessageEntity


class CreateMessage:
    def __init__(
            self, conversation_repository: ConversationRepositoryContract, message_repository: MessageRepositoryContract
    ):
        self._conversation_repository = conversation_repository
        self._message_repository = message_repository

    def create(self, webhook_dto: WebhookInputDTO) -> MessageEntity:
        conversation = self._get_open_conversation(conversation_id=webhook_dto.data.get('conversation_id'))

        message = MessageEntity(
            id=webhook_dto.data.get('id'),
            conversation=conversation,
            content=webhook_dto.data.get('content'),
            direction=MessageDirection(webhook_dto.data.get('direction')),
            external_timestamp=webhook_dto.timestamp,
        )

        self._validate_message(message_id=message.id)

        created_message = self._message_repository.create_message(message)

        return created_message

    def _get_open_conversation(self, conversation_id: UUID) -> ConversationEntity:
        conversation = self._conversation_repository.get_conversation_by_id(conversation_id)
        conversation.status_must_be_open()

        return conversation

    def _validate_message(self, message_id: UUID) -> None:
        message_already_exists = self._message_repository.get_message_by_id(message_id, raise_exception=False)

        if message_already_exists:
            # TODO: refact
            # TODO: add log
            raise APIException(detail='Message already exist')
