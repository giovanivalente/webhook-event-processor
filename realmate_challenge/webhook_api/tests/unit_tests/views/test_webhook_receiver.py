from unittest.mock import Mock, patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class TestWebhookReceiverAPIView:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('webhook_api:webhook')

    @patch('realmate_challenge.webhook_api.factory.ConversationFactory.make_webhook_event_handler', Mock())
    def test_should_return_successful_response(self, new_conversation_input_data):
        response = self.client.post(self.url, data=new_conversation_input_data, format='json')

        assert response.status_code == status.HTTP_204_NO_CONTENT

    @patch('realmate_challenge.webhook_api.factory.ConversationFactory.make_webhook_event_handler', Mock())
    def test_should_raise_error_if_type_is_not_provided(self, new_received_message_input_data):
        del new_received_message_input_data['type']

        response = self.client.post(self.url, data=new_received_message_input_data, format='json')

        field = response.json().get('errors', {})[0].get('details', {})[0].get('field')
        message = response.json().get('errors', {})[0].get('details', {})[0].get('message')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert field == 'type'
        assert message == 'This field is required.'

    @patch('realmate_challenge.webhook_api.factory.ConversationFactory.make_webhook_event_handler', Mock())
    def test_should_raise_error_if_type_is_not_supported(self, new_received_message_input_data):
        expected_type = 'UNKNOW_TYPE'
        new_received_message_input_data['type'] = expected_type
        response = self.client.post(self.url, data=new_received_message_input_data, format='json')

        field = response.json().get('errors', {})[0].get('details', {})[0].get('field')
        message = response.json().get('errors', {})[0].get('details', {})[0].get('message')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert field == 'type'
        assert message == f'"{expected_type}" is not a valid choice.'

    @patch('realmate_challenge.webhook_api.factory.ConversationFactory.make_webhook_event_handler', Mock())
    def test_should_raise_error_if_timestamp_is_not_provided(self, new_received_message_input_data):
        del new_received_message_input_data['timestamp']

        response = self.client.post(self.url, data=new_received_message_input_data, format='json')

        field = response.json().get('errors', {})[0].get('details', {})[0].get('field')
        message = response.json().get('errors', {})[0].get('details', {})[0].get('message')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert field == 'timestamp'
        assert message == 'This field is required.'

    @patch('realmate_challenge.webhook_api.factory.ConversationFactory.make_webhook_event_handler', Mock())
    def test_should_raise_error_if_timestamp_format_is_not_supported(self, new_received_message_input_data):
        new_received_message_input_data['timestamp'] = 'other_timestamp_format'

        response = self.client.post(self.url, data=new_received_message_input_data, format='json')

        field = response.json().get('errors', {})[0].get('details', {})[0].get('field')
        message = response.json().get('errors', {})[0].get('details', {})[0].get('message')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert field == 'timestamp'
        assert message == (
            'Datetime has wrong format. Use one of these formats instead: '
            'YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].'
        )

    @patch('realmate_challenge.webhook_api.factory.ConversationFactory.make_webhook_event_handler', Mock())
    def test_should_raise_error_if_data_is_not_provided(self, new_received_message_input_data):
        del new_received_message_input_data['data']

        response = self.client.post(self.url, data=new_received_message_input_data, format='json')

        field = response.json().get('errors', {})[0].get('details', {})[0].get('field')
        message = response.json().get('errors', {})[0].get('details', {})[0].get('message')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert field == 'data'
        assert message == 'This field is required.'

    @patch('realmate_challenge.webhook_api.factory.ConversationFactory.make_webhook_event_handler', Mock())
    def test_should_raise_error_if_data_id_is_not_provided(self, new_received_message_input_data):
        del new_received_message_input_data['data']['id']

        response = self.client.post(self.url, data=new_received_message_input_data, format='json')

        field = response.json().get('errors', {})[0].get('details', {})[0].get('field')
        message = response.json().get('errors', {})[0].get('details', {})[0].get('message')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert field == 'data.id'
        assert message == 'This field is required.'

    @patch('realmate_challenge.webhook_api.factory.ConversationFactory.make_webhook_event_handler', Mock())
    def test_should_raise_error_if_data_id_is_not_uuid_format(self, new_received_message_input_data):
        new_received_message_input_data['data']['id'] = 'invalid_uuid_format'

        response = self.client.post(self.url, data=new_received_message_input_data, format='json')

        field = response.json().get('errors', {})[0].get('details', {})[0].get('field')
        message = response.json().get('errors', {})[0].get('details', {})[0].get('message')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert field == 'data.id'
        assert message == 'Must be a valid UUID.'

    @patch('realmate_challenge.webhook_api.factory.ConversationFactory.make_webhook_event_handler', Mock())
    def test_should_raise_error_if_type_is_new_message_and_direction_is_not_provided(
        self, new_received_message_input_data
    ):
        del new_received_message_input_data['data']['direction']

        response = self.client.post(self.url, data=new_received_message_input_data, format='json')

        field = response.json().get('errors', {})[0].get('details', {})[0].get('field')
        message = response.json().get('errors', {})[0].get('details', {})[0].get('message')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert field == 'direction'
        assert message == 'This field is required.'

    @patch('realmate_challenge.webhook_api.factory.ConversationFactory.make_webhook_event_handler', Mock())
    def test_should_raise_error_if_type_is_new_message_and_direction_is_not_supported(
        self, new_received_message_input_data
    ):
        expected_direction = 'invalid_direction'
        new_received_message_input_data['data']['direction'] = expected_direction

        response = self.client.post(self.url, data=new_received_message_input_data, format='json')

        field = response.json().get('errors', {})[0].get('details', {})[0].get('field')
        message = response.json().get('errors', {})[0].get('details', {})[0].get('message')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert field == 'data.direction'
        assert message == f'"{expected_direction}" is not a valid choice.'

    @patch('realmate_challenge.webhook_api.factory.ConversationFactory.make_webhook_event_handler', Mock())
    def test_should_raise_error_if_type_is_new_message_and_content_is_not_provided(
        self, new_received_message_input_data
    ):
        del new_received_message_input_data['data']['content']

        response = self.client.post(self.url, data=new_received_message_input_data, format='json')

        field = response.json().get('errors', {})[0].get('details', {})[0].get('field')
        message = response.json().get('errors', {})[0].get('details', {})[0].get('message')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert field == 'content'
        assert message == 'This field is required.'

    @patch('realmate_challenge.webhook_api.factory.ConversationFactory.make_webhook_event_handler', Mock())
    def test_should_raise_error_if_type_is_new_message_and_conversation_id_is_not_provided(
        self, new_received_message_input_data
    ):
        del new_received_message_input_data['data']['conversation_id']

        response = self.client.post(self.url, data=new_received_message_input_data, format='json')

        field = response.json().get('errors', {})[0].get('details', {})[0].get('field')
        message = response.json().get('errors', {})[0].get('details', {})[0].get('message')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert field == 'conversation_id'
        assert message == 'This field is required.'
