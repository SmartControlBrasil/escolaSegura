from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.integrations.interfaces.views import IntegrationProviderViewSet, WebhookEventViewSet

router = DefaultRouter()
router.register('providers', IntegrationProviderViewSet)
router.register('webhooks', WebhookEventViewSet)
urlpatterns = [path('', include(router.urls))]
