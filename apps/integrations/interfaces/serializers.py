from rest_framework import serializers
from apps.integrations.infrastructure.models import IntegrationProvider, WebhookEvent

class IntegrationProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegrationProvider
        fields = '__all__'

class WebhookEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookEvent
        fields = '__all__'
