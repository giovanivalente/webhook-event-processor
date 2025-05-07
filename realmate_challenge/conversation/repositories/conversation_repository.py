from uuid import UUID

from rest_framework.exceptions import ValidationError

from realmate_challenge.conversation.contracts.repositories.conversation_repository_contract import (
    ConversationRepositoryContract,
)
from realmate_challenge.conversation.entities.conversation_entity import ConversationEntity
from realmate_challenge.conversation.entities.enuns import ConversationStatus
from realmate_challenge.conversation.models import Conversation as ORMConversation
from realmate_challenge.shared.repository import BaseRepository


class ConversationRepository(BaseRepository[ORMConversation], ConversationRepositoryContract):
    model = ORMConversation

    def _model_to_entity(self, model_object: ORMConversation) -> ConversationEntity:
        return ConversationEntity(
            id=model_object.id,
            status=ConversationStatus(model_object.status),
            external_timestamp=model_object.external_timestamp,
            created_at=model_object.created_at,
            updated_at=model_object.updated_at,
        )

    def create_conversation(self, conversation: ConversationEntity) -> ConversationEntity:
        conversation: ORMConversation = self.create(
            id=conversation.id, status=conversation.status.value, external_timestamp=conversation.external_timestamp
        )

        return self._model_to_entity(conversation)

    def get_conversation_by_id(self, conversation_id: UUID, raise_exception: bool = True) -> ConversationEntity | None:
        conversation = self.safe_get(id=conversation_id)
        if not conversation and raise_exception:
            # TODO: refact
            # TODO: add log
            raise ValidationError(detail=f'Conversation {conversation_id} not found.')

        return self._model_to_entity(conversation) if conversation else None

    def update_conversation(self, conversation: ConversationEntity, **kwargs) -> ConversationEntity:
        model_object = self.safe_get(id=conversation.id)
        updated_conversation = self.update(model_object, **kwargs)

        return self._model_to_entity(updated_conversation)
