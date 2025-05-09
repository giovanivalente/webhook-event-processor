from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from realmate_challenge.webhook_api.entities.enuns import ConversationStatus
from realmate_challenge.webhook_api.tests.factories import ConversationFactory, MessageFactory


class TestGetConversations:
    def setup_method(self):
        self.conversation_id = uuid4()
        self.client = APIClient()
        self.url = reverse('webhook_api:webhook-detail', args=[self.conversation_id])

    @pytest.mark.django_db
    def test_should_return_a_conversation(self):
        conversation = ConversationFactory(id=self.conversation_id)
        MessageFactory.create_batch(4, conversation=conversation)

        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('id') == str(conversation.id)
        assert response.json().get('status') == conversation.status
        assert response.json().get('count') == conversation.messages.count()
        assert len(response.json().get('messages')) == conversation.messages.count()

    @pytest.mark.django_db
    def test_should_rise_error_when_url_id_is_not_a_valid_uuid(self):
        url = reverse('webhook_api:webhook-detail', args=['non_uuid_format'])

        response = self.client.get(url)

        expected_message_error = response.json().get('errors')[0].get('details').get('message')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_message_error == 'Invalid UUID format.'

    @pytest.mark.django_db
    def test_should_rise_conversation_not_found(self):
        response = self.client.get(self.url)

        expected_message_error = response.json().get('errors')[0].get('details').get('message')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert expected_message_error == 'It was not found a conversation for this conversation id.'
