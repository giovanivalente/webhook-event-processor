from abc import ABC, abstractmethod
from uuid import UUID

from realmate_challenge.conversation.entities.conversation_entity import ConversationEntity


class ConversationRepositoryContract(ABC):
    @abstractmethod
    def create_conversation(self, conversation_entity: ConversationEntity) -> ConversationEntity:
        pass

    @abstractmethod
    def get_conversation_by_id(self, conversation_id: UUID, raise_exception: bool = True) -> ConversationEntity:
        pass

    @abstractmethod
    def update_conversation(self, conversation: ConversationEntity, **kwargs) -> ConversationEntity:
        pass
