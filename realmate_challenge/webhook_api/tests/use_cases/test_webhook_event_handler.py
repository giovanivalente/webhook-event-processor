from datetime import datetime
from unittest.mock import Mock

import pytest

from realmate_challenge.shared.exception import RealmateAPIError
from realmate_challenge.webhook_api.dtos.webhook_dto import WebhookInputDTO
from realmate_challenge.webhook_api.factory import ConversationFactory


class TestProcessWebhook:
    @pytest.fixture
    def sut(self):
        sut = ConversationFactory.make_webhook_event_handler()
        sut._create_conversation = Mock()
        sut._create_message = Mock()
        sut._close_conversation = Mock()
        return sut

    def test_should_call_create_conversation_with_correct_params(self, sut, new_conversation_webhook_input_dto):
        sut.process_webhook(new_conversation_webhook_input_dto)

        sut._create_conversation.create_new_conversation.assert_called_once_with(new_conversation_webhook_input_dto)

    def test_should_call_create_message_with_correct_params(self, sut, new_message_webhook_input_dto):
        sut.process_webhook(new_message_webhook_input_dto)

        sut._create_message.create_new_message.assert_called_once_with(new_message_webhook_input_dto)

    def test_should_call_close_conversation_with_correct_params(self, sut, close_conversation_webhook_input_dto):
        sut.process_webhook(close_conversation_webhook_input_dto)

        sut._close_conversation.close_conversation.assert_called_once_with(close_conversation_webhook_input_dto)

    def test_should_raise_error_if_event_type_is_not_supported(self, sut):
        webhook_dto = WebhookInputDTO(type='UNKNOW_TYPE', timestamp=datetime.now(), data={})

        with pytest.raises(RealmateAPIError):
            sut.process_webhook(webhook_dto)
