from realmate_challenge.shared.enum import BaseEnum


class EventType(BaseEnum):
    NEW_CONVERSATION = 'NEW_CONVERSATION'
    NEW_MESSAGE = 'NEW_MESSAGE'
    CLOSE_CONVERSATION = 'CLOSE_CONVERSATION'


class ConversationStatus(BaseEnum):
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'


class MessageDirection(BaseEnum):
    SENT = 'SENT'
    RECEIVED = 'RECEIVED'
