from django.urls import path

from realmate_challenge.webhook_api.views.webhook_receiver import WebhookReceiverAPIView

app_name = 'webhook_api'

urlpatterns = [
    path('webhook/', WebhookReceiverAPIView.as_view(), name='webhook'),
]
