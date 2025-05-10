from uuid import uuid4

from django.core.management.base import BaseCommand
from django.utils import timezone

from realmate_challenge.webhook_api.models import Conversation
from realmate_challenge.webhook_api.tests.factories import MessageFactory


class Command(BaseCommand):
    help = 'Populate database with conversations and fake messages.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--conversations',
            type=int,
            default=1,
            help='Number of conversations to be created (default: 1)',
        )
        parser.add_argument(
            '--messages',
            type=int,
            default=5,
            help='Number of messages per conversation (default: 5)',
        )

    def handle(self, *args, **options):
        num_conversations = options['conversations']
        num_messages = options['messages']

        for _ in range(num_conversations):
            conversation = Conversation.objects.create(
                id=uuid4(),
                status='OPEN',
                external_timestamp=timezone.now(),
            )
            MessageFactory.create_batch(num_messages, conversation=conversation)

        self.stdout.write(
            self.style.SUCCESS(f'{num_conversations} conversation(s) created with {num_messages} message(s) each.')
        )
