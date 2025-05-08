import logging
from uuid import UUID

from realmate_challenge.shared.repository import BaseRepository
from realmate_challenge.webhook_api.contracts.repositories.message_repository_contract import MessageRepositoryContract
from realmate_challenge.webhook_api.entities.message_entity import MessageEntity
from realmate_challenge.webhook_api.exceptions import MessageNotFound
from realmate_challenge.webhook_api.mapper import conversation_entity_to_model, message_model_to_entity
from realmate_challenge.webhook_api.models import Message as ORMMessage

logger = logging.getLogger(__name__)


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

        logger.info(f"A new message '{message.id}' was created.")
        return message_model_to_entity(message)

    def get_message_by_id(self, message_id: UUID, raise_exception: bool = True) -> MessageEntity | None:
        message = self.safe_get(id=message_id)
        if not message and raise_exception:
            logger.error(f"Message with ID '{message.id}' is not found.")
            raise MessageNotFound()

        return message_model_to_entity(message) if message else None
