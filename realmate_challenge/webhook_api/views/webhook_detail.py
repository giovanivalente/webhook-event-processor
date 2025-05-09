from uuid import UUID

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from realmate_challenge.shared.pagination import CustomPagination
from realmate_challenge.shared.schema_exceptions import STANDARD_ERROR_RESPONSES
from realmate_challenge.webhook_api.factory import ConversationFactory
from realmate_challenge.webhook_api.serializers.webhook_detail import ConversationOutputSerializer, \
    MessageOutputSerializer


class WebhookDetailAPIView(APIView):
    def __init__(self):
        super().__init__()
        self.conversation_service = ConversationFactory.make_conversation_detail()
        self.pagination_class = CustomPagination

    @extend_schema(
        parameters=[
            OpenApiParameter(name='page', type=int, required=False, description='Page number'),
            OpenApiParameter(name='page_size', type=int, required=False, description='Number of items per page')
        ],
        responses={200: ConversationOutputSerializer, **STANDARD_ERROR_RESPONSES},
        summary='Detail Conversation',
        description='Endpoint to list conversations by id.',
    )
    def get(self, request, conversation_id: str | UUID) -> Response:
        conversation = self.conversation_service.get_conversation_by_id(conversation_id)

        sorted_messages = sorted(conversation.messages, key=lambda x: x.external_timestamp)

        paginator = self.pagination_class()
        paginated = paginator.paginate_queryset(sorted_messages, request, view=self)

        conversation_data = ConversationOutputSerializer(conversation, context={"paginated_messages": paginated}).data
        message_data = MessageOutputSerializer(paginated, many=True).data

        paginated_data = paginator.build_conversation_response_data(conversation_data, message_data)

        return Response(data=paginated_data, status=status.HTTP_200_OK)
