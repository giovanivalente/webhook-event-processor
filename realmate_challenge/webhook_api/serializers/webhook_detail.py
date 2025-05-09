from rest_framework import serializers

from realmate_challenge.webhook_api.entities.conversation_entity import ConversationEntity


class MessageOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    content = serializers.CharField()
    direction = serializers.CharField()
    timestamp = serializers.DateTimeField(source='external_timestamp')


class ConversationOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    status = serializers.CharField()
    messages = MessageOutputSerializer(many=True)

    def to_representation(self, instance: ConversationEntity):
        messages = self.context.get("paginated_messages")

        return {
            "id": instance.id,
            "status": instance.status.value,
            "messages": MessageOutputSerializer(messages, many=True).data,
        }
