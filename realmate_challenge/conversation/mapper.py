from realmate_challenge.conversation.entities.conversation_entity import ConversationEntity
from realmate_challenge.conversation.entities.enuns import ConversationStatus, MessageDirection
from realmate_challenge.conversation.entities.message_entity import MessageEntity
from realmate_challenge.conversation.models import Conversation as ORMConversation
from realmate_challenge.conversation.models import Message as ORMMessage


def conversation_model_to_entity(model_object: ORMConversation) -> ConversationEntity:
    return ConversationEntity(
        id=model_object.id,
        status=ConversationStatus(model_object.status),
        external_timestamp=model_object.external_timestamp,
        created_at=model_object.created_at,
        updated_at=model_object.updated_at,
    )


def conversation_entity_to_model(entity: ConversationEntity) -> ORMConversation:
    return ORMConversation(
        id=entity.id,
        status=entity.status.value,
        external_timestamp=entity.external_timestamp,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def message_model_to_entity(model_object: ORMMessage) -> MessageEntity:
    return MessageEntity(
        id=model_object.id,
        conversation=conversation_model_to_entity(model_object.conversation),
        content=model_object.content,
        direction=MessageDirection(model_object.direction),
        external_timestamp=model_object.external_timestamp,
        created_at=model_object.created_at,
        updated_at=model_object.updated_at,
    )
