from datetime import datetime
from uuid import uuid4

import pytest

from realmate_challenge.webhook_api.dtos.webhook_dto import WebhookInputDTO
from realmate_challenge.webhook_api.entities.enuns import EventType, MessageDirection


@pytest.fixture
def new_conversation_webhook_input_dto():
    return WebhookInputDTO(type=EventType.NEW_CONVERSATION, timestamp=datetime.now(), data={'id': uuid4()})


@pytest.fixture
def close_conversation_webhook_input_dto():
    return WebhookInputDTO(type=EventType.CLOSE_CONVERSATION, timestamp=datetime.now(), data={'id': uuid4()})


@pytest.fixture
def new_message_webhook_input_dto():
    return WebhookInputDTO(
        type=EventType.NEW_MESSAGE,
        timestamp=datetime.now(),
        data={
            'id': uuid4(),
            'direction': MessageDirection.SENT,
            'content': 'content message',
            'conversation_id': uuid4(),
        },
    )


@pytest.fixture
def new_conversation_input_data():
    return {
        'type': 'NEW_CONVERSATION',
        'timestamp': '2025-02-21T10:20:41.349308',
        'data': {'id': '6a41b347-8d80-4ce9-84ba-7af66f369f6a'},
    }


@pytest.fixture
def close_conversation_input_data():
    return {
        'type': 'CLOSE_CONVERSATION',
        'timestamp': '2025-02-21T10:20:45.349308',
        'data': {'id': '6a41b347-8d80-4ce9-84ba-7af66f369f6a'},
    }


@pytest.fixture
def new_received_message_input_data():
    return {
        'type': 'NEW_MESSAGE',
        'timestamp': '2025-02-21T10:20:42.349308',
        'data': {
            'id': '49108c71-4dca-4af3-9f32-61bc745926e2',
            'direction': 'RECEIVED',
            'content': 'Olá, tudo bem?',
            'conversation_id': '6a41b347-8d80-4ce9-84ba-7af66f369f6a',
        },
    }


@pytest.fixture
def new_sent_message_input_data():
    return {
        'type': 'NEW_MESSAGE',
        'timestamp': '2025-02-21T10:20:44.349308',
        'data': {
            'id': '16b63b04-60de-4257-b1a1-20a5154abc6d',
            'direction': 'SENT',
            'content': 'Tudo ótimo e você?',
            'conversation_id': '6a41b347-8d80-4ce9-84ba-7af66f369f6a',
        },
    }
