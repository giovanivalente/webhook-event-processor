from unittest.mock import Mock
from uuid import uuid4

import pytest

from realmate_challenge.shared.exception import RealmateAPIError
from realmate_challenge.webhook_api.entities.conversation_entity import ConversationEntity
from realmate_challenge.webhook_api.entities.enuns import ConversationStatus
from realmate_challenge.webhook_api.entities.message_entity import MessageEntity
from realmate_challenge.webhook_api.factory import ConversationFactory
from realmate_challenge.webhook_api.mapper import webhook_dto_to_message_entity


class TestCreateNewConversation:
    @pytest.fixture
    def sut(self):
        sut = ConversationFactory.make_create_message()
        sut._get_open_conversation = Mock(return_value=self.conversation)
        sut._validate_message = Mock()
        sut._message_repository.create_message = Mock()
        return sut

    def setup_method(self):
        self.conversation = Mock(spec=ConversationEntity)

    def test_should_call_get_open_conversation_with_correct_params(self, sut, new_message_webhook_input_dto):
        conversation_id = new_message_webhook_input_dto.data.get('conversation_id')

        sut.create_new_message(new_message_webhook_input_dto)

        sut._get_open_conversation.assert_called_once_with(conversation_id=conversation_id)

    def test_should_call_validate_message_with_correct_params(self, sut, new_message_webhook_input_dto):
        message = webhook_dto_to_message_entity(new_message_webhook_input_dto, self.conversation)

        sut.create_new_message(new_message_webhook_input_dto)

        sut._validate_message.assert_called_once_with(message_id=message.id)

    def test_should_call_create_message_with_correct_params(self, sut, new_message_webhook_input_dto):
        message = webhook_dto_to_message_entity(new_message_webhook_input_dto, self.conversation)

        sut.create_new_message(new_message_webhook_input_dto)

        sut._message_repository.create_message.assert_called_once_with(message)


class TestGetOpenConversation:
    @pytest.fixture
    def sut(self):
        sut = ConversationFactory.make_create_message()
        sut._conversation_repository.get_conversation_by_id = Mock(return_value=self.conversation)
        return sut

    def setup_method(self):
        self.conversation = Mock(spec=ConversationEntity)
        self.conversation.id = uuid4()
        self.conversation.status = ConversationStatus.CLOSED

    def test_should_call_get_conversation_by_id_with_correct_params(self, sut):
        sut._get_open_conversation(conversation_id=self.conversation.id)

        sut._conversation_repository.get_conversation_by_id.assert_called_once_with(self.conversation.id)


class TestValidateConversation:
    @pytest.fixture
    def sut(self):
        sut = ConversationFactory.make_create_message()
        sut._message_repository.get_message_by_id = Mock(return_value=None)
        return sut

    def setup_method(self):
        self.message = Mock(spec=MessageEntity)
        self.message.id = uuid4()

    def test_should_call_get_message_by_id_with_correct_params(self, sut):
        sut._validate_message(message_id=self.message.id)

        sut._message_repository.get_message_by_id.assert_called_once_with(self.message.id, raise_exception=False)

    def test_should_raise_error_if_message_already_exists(self, sut):
        sut._message_repository.get_message_by_id.return_value = self.message

        with pytest.raises(RealmateAPIError):
            sut._validate_message(message_id=self.message.id)
