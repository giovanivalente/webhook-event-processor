from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from realmate_challenge.webhook_api.dtos.webhook_dto import WebhookInputDTO
from realmate_challenge.webhook_api.entities.enuns import EventType
from realmate_challenge.webhook_api.factory import ConversationFactory
from realmate_challenge.webhook_api.serializers.webhook_receiver import WebhookReceiverSerializer


class WebhookReceiverAPIView(APIView):
    def __init__(self):
        super().__init__()
        self.webhook_event_handler = ConversationFactory.make_webhook_event_handler()

    def post(self, request):
        serializer = WebhookReceiverSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        webhook_dto = WebhookInputDTO(
            type=EventType(serializer.validated_data.get('type')),
            timestamp=serializer.validated_data.get('timestamp'),
            data=serializer.validated_data.get('data'),
        )

        self.webhook_event_handler.process_webhook(webhook_dto)

        return Response(status=status.HTTP_204_NO_CONTENT)
