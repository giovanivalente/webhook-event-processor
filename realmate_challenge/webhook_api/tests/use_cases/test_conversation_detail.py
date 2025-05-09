from unittest.mock import Mock
from uuid import uuid4

import pytest

from realmate_challenge.webhook_api.entities.conversation_entity import ConversationEntity
from realmate_challenge.webhook_api.factory import ConversationFactory


class TestGetConversationById:
    @pytest.fixture
    def sut(self):
        sut = ConversationFactory.make_conversation_detail()
        sut._conversation_repository.get_conversation_by_id = Mock(return_value=self.conversation)
        return sut

    def setup_method(self):
        self.conversation = Mock(spec=ConversationEntity)
        self.conversation.id = uuid4()

    def test_should_call_get_conversation_by_id_with_correct_params(self, sut):
        sut.get_conversation_by_id(conversation_id=self.conversation.id)

        sut._conversation_repository.get_conversation_by_id.assert_called_once_with(self.conversation.id)

    def test_should_return_conversation_entity(self, sut):
        conversation_entity = sut.get_conversation_by_id(conversation_id=str(self.conversation.id))

        assert isinstance(conversation_entity, ConversationEntity)
