from unittest.mock import Mock
from uuid import uuid4

import pytest

from realmate_challenge.shared.exception import RealmateAPIError
from realmate_challenge.webhook_api.entities.conversation_entity import ConversationEntity
from realmate_challenge.webhook_api.entities.enuns import ConversationStatus
from realmate_challenge.webhook_api.factory import ConversationFactory


class TestCloseConversation:
    @pytest.fixture
    def sut(self):
        sut = ConversationFactory.make_close_conversation()
        sut._conversation_repository.get_conversation_by_id = Mock(return_value=self.open_conversation)
        sut._conversation_repository.update_conversation = Mock()
        sut._validate_conversation = Mock()
        return sut

    def setup_method(self):
        self.open_conversation = Mock(spec=ConversationEntity)

    def test_should_call_get_conversation_by_id_with_correct_params(self, sut, close_conversation_webhook_input_dto):
        conversation_id = close_conversation_webhook_input_dto.data.get('id')

        sut.close_conversation(close_conversation_webhook_input_dto)

        sut._conversation_repository.get_conversation_by_id.assert_called_once_with(conversation_id)

    def test_should_call_validate_conversation_with_correct_params(self, sut, close_conversation_webhook_input_dto):
        sut.close_conversation(close_conversation_webhook_input_dto)

        sut._validate_conversation.assert_called_once_with(self.open_conversation)

    def test_should_call_update_conversation_with_correct_params(self, sut, close_conversation_webhook_input_dto):
        sut.close_conversation(close_conversation_webhook_input_dto)

        sut._conversation_repository.update_conversation.assert_called_once_with(
            conversation=self.open_conversation, status=ConversationStatus.CLOSED.value
        )


class TestValidateConversation:
    @pytest.fixture
    def sut(self):
        sut = ConversationFactory.make_close_conversation()
        return sut

    def setup_method(self):
        self.closed_conversation = Mock(spec=ConversationEntity)
        self.closed_conversation.status = ConversationStatus.CLOSED
        self.closed_conversation.id = uuid4()

    def test_should_raise_error_if_conversation_already_closed(self, sut):
        with pytest.raises(RealmateAPIError):
            sut._validate_conversation(conversation=self.closed_conversation)
