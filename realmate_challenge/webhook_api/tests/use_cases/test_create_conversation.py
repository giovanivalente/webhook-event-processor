from unittest.mock import Mock

import pytest

from realmate_challenge.shared.exception import RealmateAPIError
from realmate_challenge.webhook_api.factory import ConversationFactory
from realmate_challenge.webhook_api.mapper import webhook_dto_to_open_conversation_entity


class TestCreateNewConversation:
    @pytest.fixture
    def sut(self):
        sut = ConversationFactory.make_create_conversation()
        sut._conversation_repository.create_conversation = Mock()
        sut._validate_conversation = Mock()
        return sut

    def test_should_call_validate_conversation_with_correct_params(self, sut, new_conversation_webhook_input_dto):
        conversation_id = new_conversation_webhook_input_dto.data.get('id')

        sut.create_new_conversation(new_conversation_webhook_input_dto)

        sut._validate_conversation.assert_called_once_with(conversation_id=conversation_id)

    def test_should_call_create_conversation_with_correct_params(self, sut, new_conversation_webhook_input_dto):
        conversation = webhook_dto_to_open_conversation_entity(new_conversation_webhook_input_dto)

        sut.create_new_conversation(new_conversation_webhook_input_dto)

        sut._conversation_repository.create_conversation.assert_called_once_with(conversation)


class TestValidateConversation:
    @pytest.fixture
    def sut(self):
        sut = ConversationFactory.make_create_conversation()
        sut._conversation_repository.get_conversation_by_id = Mock(return_value=None)
        return sut

    def test_should_call_get_conversation_by_id_with_correct_params(self, sut, new_conversation_webhook_input_dto):
        conversation = webhook_dto_to_open_conversation_entity(new_conversation_webhook_input_dto)

        sut._validate_conversation(conversation_id=conversation.id)

        sut._conversation_repository.get_conversation_by_id.assert_called_once_with(
            conversation.id, raise_exception=False
        )

    def test_should_raise_error_if_conversation_already_exists(self, sut, new_conversation_webhook_input_dto):
        conversation = webhook_dto_to_open_conversation_entity(new_conversation_webhook_input_dto)
        sut._conversation_repository.get_conversation_by_id.return_value = conversation

        with pytest.raises(RealmateAPIError):
            sut._validate_conversation(conversation_id=conversation.id)
