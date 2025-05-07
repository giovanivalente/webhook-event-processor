from rest_framework.exceptions import ValidationError

from realmate_challenge.conversation.dtos.webhook_dto import WebhookInputDTO
from realmate_challenge.conversation.entities.enuns import EventType
from realmate_challenge.conversation.use_cases.close_conversation import CloseConversation
from realmate_challenge.conversation.use_cases.create_conversation import CreateConversation
from realmate_challenge.conversation.use_cases.create_message import CreateMessage


class WebhookEventHandler:
    def __init__(
        self,
        create_conversation: CreateConversation,
        create_message: CreateMessage,
        close_conversation: CloseConversation,
    ):
        self._create_conversation = create_conversation
        self._create_message = create_message
        self._close_conversation = close_conversation

    def process_webhook(self, webhook_dto: WebhookInputDTO) -> None:
        event_type = webhook_dto.type

        if event_type == EventType.NEW_CONVERSATION:
            self._create_conversation.create(webhook_dto)

        elif event_type == EventType.NEW_MESSAGE:
            self._create_message.create(webhook_dto)

        elif event_type == EventType.CLOSE_CONVERSATION:
            self._close_conversation.close(webhook_dto)

        else:
            # TODO: refact
            # TODO: add log
            raise ValidationError(detail=f'Unknow Event: {event_type}')
