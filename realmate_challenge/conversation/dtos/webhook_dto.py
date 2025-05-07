from dataclasses import dataclass
from xmlrpc.client import DateTime

from realmate_challenge.conversation.entities.enuns import EventType


@dataclass
class WebhookInputDTO:
    type: EventType
    timestamp: DateTime
    data: dict
