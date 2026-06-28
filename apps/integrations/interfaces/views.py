from rest_framework import viewsets
from apps.integrations.infrastructure.models import IntegrationProvider, WebhookEvent
from apps.integrations.interfaces.serializers import IntegrationProviderSerializer, WebhookEventSerializer

class IntegrationProviderViewSet(viewsets.ModelViewSet):
    queryset = IntegrationProvider.objects.all()
    serializer_class = IntegrationProviderSerializer
    search_fields = ['name','slug']
    filterset_fields = ['is_active']

class WebhookEventViewSet(viewsets.ModelViewSet):
    queryset = WebhookEvent.objects.select_related('provider').all()
    serializer_class = WebhookEventSerializer
    search_fields = ['event_type','error_message']
    filterset_fields = ['provider','event_type','status']
