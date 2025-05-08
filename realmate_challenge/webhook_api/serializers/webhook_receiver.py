from rest_framework import serializers

from realmate_challenge.webhook_api.entities.enuns import EventType, MessageDirection


class NewConversationSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class CloseConversationSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class NewMessageSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    direction = serializers.ChoiceField(choices=MessageDirection.choices())
    content = serializers.CharField()
    conversation_id = serializers.UUIDField()


class DataSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    direction = serializers.ChoiceField(choices=MessageDirection.choices(), required=False)
    content = serializers.CharField(required=False)
    conversation_id = serializers.UUIDField(required=False)


class WebhookReceiverSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=EventType.choices())
    timestamp = serializers.DateTimeField()
    data = DataSerializer()

    def validate(self, attrs):
        event_type = EventType(attrs.get('type'))
        raw_data = attrs.get('data')

        serializer_map = {
            EventType.NEW_CONVERSATION: NewConversationSerializer,
            EventType.NEW_MESSAGE: NewMessageSerializer,
            EventType.CLOSE_CONVERSATION: CloseConversationSerializer,
        }

        serializer_class = serializer_map.get(event_type)
        event_serializer = serializer_class(data=raw_data)
        event_serializer.is_valid(raise_exception=True)

        attrs['data'] = event_serializer.validated_data

        return attrs
