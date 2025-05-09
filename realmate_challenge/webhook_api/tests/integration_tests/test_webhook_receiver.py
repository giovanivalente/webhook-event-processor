import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from realmate_challenge.webhook_api.entities.enuns import ConversationStatus
from realmate_challenge.webhook_api.models import Conversation, Message
from realmate_challenge.webhook_api.tests.factories import ConversationFactory, MessageFactory


class TestCreateConversation:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('webhook_api:webhook')

    @pytest.mark.django_db
    def test_should_create_new_conversation(self, new_conversation_input_data):
        conversation_id = new_conversation_input_data.get('data', {}).get('id')

        response = self.client.post(self.url, data=new_conversation_input_data, format='json')

        created_conversation = Conversation.objects.get(id=conversation_id)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert str(created_conversation.id) == conversation_id

    @pytest.mark.django_db
    def test_should_rise_conversation_already_exists(self, new_conversation_input_data):
        existent_conversation = ConversationFactory()

        new_conversation_input_data['data']['id'] = str(existent_conversation.id)

        response = self.client.post(self.url, data=new_conversation_input_data, format='json')
        expected_message_error = response.json().get('errors')[0].get('details').get('message')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_message_error == 'The conversation with the given ID already exists.'


class TestCloseConversation:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('webhook_api:webhook')

    @pytest.mark.django_db
    def test_should_close_conversation(self, close_conversation_input_data):
        opened_conversation = ConversationFactory(status=ConversationStatus.OPEN)
        close_conversation_input_data['data']['id'] = str(opened_conversation.id)

        response = self.client.post(self.url, data=close_conversation_input_data, format='json')

        closed_conversation = Conversation.objects.get(id=opened_conversation.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert closed_conversation.status == ConversationStatus.CLOSED

    @pytest.mark.django_db
    def test_should_raise_conversation_not_found(self, close_conversation_input_data):
        ConversationFactory(status=ConversationStatus.OPEN)

        response = self.client.post(self.url, data=close_conversation_input_data, format='json')

        expected_message_error = response.json().get('errors')[0].get('details').get('message')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert expected_message_error == 'It was not found a conversation for this conversation id.'

    @pytest.mark.django_db
    def test_should_raise_conversation_status_is_already_closed(self, close_conversation_input_data):
        closed_conversation = ConversationFactory(status=ConversationStatus.CLOSED)
        close_conversation_input_data['data']['id'] = str(closed_conversation.id)

        response = self.client.post(self.url, data=close_conversation_input_data, format='json')

        expected_message_error = response.json().get('errors')[0].get('details').get('message')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_message_error == 'A conversation with the given ID is already closed.'


class TestCreateNewMessage:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('webhook_api:webhook')

    @pytest.mark.django_db
    def test_should_create_a_new_message(self, new_received_message_input_data):
        opened_conversation = ConversationFactory(status=ConversationStatus.OPEN)
        new_received_message_input_data['data']['conversation_id'] = str(opened_conversation.id)

        message_id = new_received_message_input_data['data']['id']

        response = self.client.post(self.url, data=new_received_message_input_data, format='json')

        new_message = Message.objects.get(id=message_id)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert str(new_message.id) == message_id
        assert opened_conversation.messages.count() == 1

    @pytest.mark.django_db
    def test_should_raise_conversation_not_found(self, new_received_message_input_data):
        response = self.client.post(self.url, data=new_received_message_input_data, format='json')

        expected_message_error = response.json().get('errors')[0].get('details').get('message')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert expected_message_error == 'It was not found a conversation for this conversation id.'

    @pytest.mark.django_db
    def test_should_raise_conversation_already_closed(self, new_received_message_input_data):
        closed_conversation = ConversationFactory(status=ConversationStatus.CLOSED)
        new_received_message_input_data['data']['conversation_id'] = str(closed_conversation.id)

        response = self.client.post(self.url, data=new_received_message_input_data, format='json')

        expected_message_error = response.json().get('errors')[0].get('details').get('message')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_message_error == 'A conversation with the given ID is already closed.'

    @pytest.mark.django_db
    def test_should_raise_message_already_exists(self, new_received_message_input_data):
        opened_conversation = ConversationFactory(status=ConversationStatus.OPEN)
        new_received_message_input_data['data']['conversation_id'] = str(opened_conversation.id)
        message_id = new_received_message_input_data['data']['id']

        MessageFactory(id=message_id)

        response = self.client.post(self.url, data=new_received_message_input_data, format='json')

        expected_message_error = response.json().get('errors')[0].get('details').get('message')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_message_error == 'The message with the given ID already exists.'
