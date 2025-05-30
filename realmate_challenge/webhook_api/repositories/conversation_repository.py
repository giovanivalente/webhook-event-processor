import logging
from uuid import UUID

from realmate_challenge.shared.repository import BaseRepository
from realmate_challenge.webhook_api.contracts.repositories.conversation_repository_contract import (
    ConversationRepositoryContract,
)
from realmate_challenge.webhook_api.entities.conversation_entity import ConversationEntity
from realmate_challenge.webhook_api.exceptions import ConversationNotFound
from realmate_challenge.webhook_api.mapper import conversation_model_to_entity
from realmate_challenge.webhook_api.models import Conversation as ORMConversation

logger = logging.getLogger(__name__)


class ConversationRepository(BaseRepository[ORMConversation], ConversationRepositoryContract):
    model = ORMConversation

    def create_conversation(self, conversation_entity: ConversationEntity) -> ConversationEntity:
        conversation: ORMConversation = self.create(
            id=conversation_entity.id,
            status=conversation_entity.status.value,
            external_timestamp=conversation_entity.external_timestamp,
        )

        logger.info(f"A new conversation '{conversation.id}' was created.")
        return conversation_model_to_entity(conversation)

    def get_conversation_by_id(self, conversation_id: UUID, raise_exception: bool = True) -> ConversationEntity | None:
        conversation = self.safe_get_with_prefetch(prefetch_fields=['messages'], id=conversation_id)
        if not conversation and raise_exception:
            logger.error(f"Conversation with ID '{conversation_id}' is not found.")
            raise ConversationNotFound()

        return conversation_model_to_entity(conversation) if conversation else None

    def update_conversation(self, conversation: ConversationEntity, **kwargs) -> ConversationEntity:
        model_object = self.safe_get(id=conversation.id)
        updated_conversation = self.update(model_object, **kwargs)

        logger.info(f"The conversation '{conversation.id}' was updated.")
        return conversation_model_to_entity(updated_conversation)
