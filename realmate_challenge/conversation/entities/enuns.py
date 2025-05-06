from realmate_challenge.shared.enum import BaseEnum


class ConversationStatus(BaseEnum):
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'


class MessageDirection(BaseEnum):
    SENT = 'SENT'
    RECEIVED = 'RECEIVED'
