from datetime import timedelta
from uuid import uuid4

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from realmate_challenge.webhook_api.entities.enuns import ConversationStatus, MessageDirection
from realmate_challenge.webhook_api.models import Conversation, Message


class ConversationFactory(DjangoModelFactory):
    class Meta:
        model = Conversation

    id = factory.LazyFunction(uuid4)
    status = factory.Iterator([choice[0] for choice in ConversationStatus.choices()])
    external_timestamp = factory.LazyFunction(lambda: timezone.now() - timedelta(days=1))
    created_at = factory.LazyFunction(lambda: timezone.now() - timedelta(hours=20))
    updated_at = factory.LazyFunction(lambda: timezone.now() - timedelta(hours=20))


class MessageFactory(DjangoModelFactory):
    class Meta:
        model = Message

    id = factory.LazyFunction(uuid4)
    conversation = factory.SubFactory(ConversationFactory)
    content = factory.Faker('text')
    direction = factory.Iterator([choice[0] for choice in MessageDirection.choices()])
    external_timestamp = factory.LazyFunction(lambda: timezone.now() - timedelta(days=1))
    created_at = factory.LazyFunction(lambda: timezone.now() - timedelta(hours=20))
    updated_at = factory.LazyFunction(lambda: timezone.now() - timedelta(hours=20))
