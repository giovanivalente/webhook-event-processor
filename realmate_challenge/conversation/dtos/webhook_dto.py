from dataclasses import dataclass
from datetime import datetime

from realmate_challenge.conversation.entities.enuns import EventType


@dataclass
class WebhookInputDTO:
    type: EventType
    timestamp: datetime
    data: dict
