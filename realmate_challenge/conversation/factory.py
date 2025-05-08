from realmate_challenge.conversation.contracts.repositories.conversation_repository_contract import (
    ConversationRepositoryContract,
)
from realmate_challenge.conversation.contracts.repositories.message_repository_contract import MessageRepositoryContract
from realmate_challenge.conversation.repositories.conversation_repository import ConversationRepository
from realmate_challenge.conversation.repositories.message_repository import MessageRepository
from realmate_challenge.conversation.use_cases.close_conversation import CloseConversation
from realmate_challenge.conversation.use_cases.create_conversation import CreateConversation
from realmate_challenge.conversation.use_cases.create_message import CreateMessage
from realmate_challenge.conversation.use_cases.webhook_event_handler import WebhookEventHandler


class ConversationFactory:
    @classmethod
    def make_conversation_repository(cls) -> ConversationRepositoryContract:
        return ConversationRepository()

    @classmethod
    def make_message_repository(cls) -> MessageRepositoryContract:
        return MessageRepository()

    @classmethod
    def make_webhook_event_handler(cls) -> WebhookEventHandler:
        return WebhookEventHandler(
            create_conversation=cls.make_create_conversation(),
            close_conversation=cls.make_close_conversation(),
            create_message=cls.make_create_message(),
        )

    @classmethod
    def make_create_conversation(cls) -> CreateConversation:
        return CreateConversation(conversation_repository=cls.make_conversation_repository())

    @classmethod
    def make_create_message(cls) -> CreateMessage:
        return CreateMessage(
            conversation_repository=cls.make_conversation_repository(), message_repository=cls.make_message_repository()
        )

    @classmethod
    def make_close_conversation(cls) -> CloseConversation:
        return CloseConversation(conversation_repository=cls.make_conversation_repository())
