from abc import ABC, abstractmethod
from uuid import UUID

from realmate_challenge.webhook_api.entities.message_entity import MessageEntity


class MessageRepositoryContract(ABC):
    @abstractmethod
    def create_message(self, message: MessageEntity) -> MessageEntity:
        pass  # pragma: no cover

    @abstractmethod
    def get_message_by_id(self, message_id: UUID, raise_exception: bool = True) -> MessageEntity | None:
        pass  # pragma: no cover
