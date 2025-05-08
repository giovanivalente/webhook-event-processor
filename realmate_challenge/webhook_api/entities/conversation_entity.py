import logging
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from realmate_challenge.shared.exception import RealmateAPIError
from realmate_challenge.webhook_api.entities.enuns import ConversationStatus

logger = logging.getLogger(__name__)


@dataclass
class ConversationEntity:
    id: UUID
    status: ConversationStatus
    external_timestamp: datetime
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def status_must_be_open(self):
        if self.status == ConversationStatus.CLOSED:
            logger.warning(f"Conversation with ID '{self.id}' is already closed.")
            raise RealmateAPIError(detail='A conversation with the given ID is already closed.')
