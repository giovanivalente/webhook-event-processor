from realmate_challenge.conversation.dtos.webhook_dto import WebhookInputDTO


class CreateMessage:
    def create(self, webhook_dto: WebhookInputDTO): ...
