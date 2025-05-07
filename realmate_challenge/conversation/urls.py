from django.urls import path

from realmate_challenge.conversation.views.webhook_receiver import WebhookReceiverAPIView

app_name = 'conversation'

urlpatterns = [
    path('webhook/', WebhookReceiverAPIView.as_view(), name='webhook'),
]
