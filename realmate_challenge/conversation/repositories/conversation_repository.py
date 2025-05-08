from uuid import UUID

from rest_framework.exceptions import APIException

from realmate_challenge.conversation.contracts.repositories.conversation_repository_contract import (
    ConversationRepositoryContract,
)
from realmate_challenge.conversation.entities.conversation_entity import ConversationEntity
from realmate_challenge.conversation.mapper import conversation_model_to_entity
from realmate_challenge.conversation.models import Conversation as ORMConversation
from realmate_challenge.shared.repository import BaseRepository


class ConversationRepository(BaseRepository[ORMConversation], ConversationRepositoryContract):
    model = ORMConversation

    def create_conversation(self, conversation_entity: ConversationEntity) -> ConversationEntity:
        conversation: ORMConversation = self.create(
            id=conversation_entity.id,
            status=conversation_entity.status.value,
            external_timestamp=conversation_entity.external_timestamp,
        )

        return conversation_model_to_entity(conversation)

    def get_conversation_by_id(self, conversation_id: UUID, raise_exception: bool = True) -> ConversationEntity | None:
        conversation = self.safe_get(id=conversation_id)
        if not conversation and raise_exception:
            # TODO: refact
            # TODO: add log
            raise APIException(detail=f'Conversation {conversation_id} not found.')

        return conversation_model_to_entity(conversation) if conversation else None

    def update_conversation(self, conversation: ConversationEntity, **kwargs) -> ConversationEntity:
        model_object = self.safe_get(id=conversation.id)
        updated_conversation = self.update(model_object, **kwargs)

        return conversation_model_to_entity(updated_conversation)
