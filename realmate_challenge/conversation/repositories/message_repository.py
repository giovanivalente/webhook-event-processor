from uuid import UUID

from rest_framework.exceptions import ValidationError, APIException

from realmate_challenge.conversation.contracts.repositories.message_repository_contract import MessageRepositoryContract
from realmate_challenge.conversation.entities.message_entity import MessageEntity
from realmate_challenge.conversation.mapper import conversation_entity_to_model, message_model_to_entity
from realmate_challenge.conversation.models import Message as ORMMessage
from realmate_challenge.shared.repository import BaseRepository


class MessageRepository(BaseRepository[ORMMessage], MessageRepositoryContract):
    model = ORMMessage

    def create_message(self, message: MessageEntity) -> MessageEntity:
        message: ORMMessage = self.create(
            id=message.id,
            conversation=conversation_entity_to_model(message.conversation),
            content=message.content,
            direction=message.direction,
            external_timestamp=message.external_timestamp,
        )

        return message_model_to_entity(message)

    def get_message_by_id(self, message_id: UUID, raise_exception: bool = True) -> MessageEntity | None:
        message = self.safe_get(id=message_id)
        if not message and raise_exception:
            # TODO: refact
            # TODO: add log
            raise APIException(detail=f'Message {message_id} not found.')

        return message_model_to_entity(message) if message else None
