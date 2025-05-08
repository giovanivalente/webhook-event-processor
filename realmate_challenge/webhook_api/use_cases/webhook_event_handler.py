import logging

from realmate_challenge.shared.exception import RealmateAPIError
from realmate_challenge.webhook_api.dtos.webhook_dto import WebhookInputDTO
from realmate_challenge.webhook_api.entities.enuns import EventType
from realmate_challenge.webhook_api.use_cases.close_conversation import CloseConversation
from realmate_challenge.webhook_api.use_cases.create_conversation import CreateConversation
from realmate_challenge.webhook_api.use_cases.create_message import CreateMessage

logger = logging.getLogger(__name__)


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
            self._create_conversation.create_new_conversation(webhook_dto)

        elif event_type == EventType.NEW_MESSAGE:
            self._create_message.create_new_message(webhook_dto)

        elif event_type == EventType.CLOSE_CONVERSATION:
            self._close_conversation.close_conversation(webhook_dto)

        else:
            logger.warning(f"The event type '{event_type}' is not supported.")
            raise RealmateAPIError(detail='The provided event type is not supported or is invalid.')
