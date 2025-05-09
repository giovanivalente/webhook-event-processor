from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from realmate_challenge.webhook_api.mapper import conversation_model_to_entity
from realmate_challenge.webhook_api.tests.factories import ConversationFactory, MessageFactory


class TestWebhookReceiverAPIView:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('webhook_api:webhook-detail', args=['id'])

    @pytest.mark.django_db
    @patch('realmate_challenge.webhook_api.factory.ConversationFactory.make_conversation_detail')
    def test_should_return_successful_response(self, mocked_conversation):
        conversation_entity = conversation_model_to_entity(ConversationFactory())
        mocked_conversation.return_value.get_conversation_by_id.return_value = conversation_entity
        conversation = mocked_conversation.return_value.get_conversation_by_id.return_value
        conversation.messages = MessageFactory.create_batch(13)

        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('count') == len(conversation.messages)
