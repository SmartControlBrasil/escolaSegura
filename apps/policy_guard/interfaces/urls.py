from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.policy_guard.interfaces.views import ConsentRecordViewSet, DataProcessingRecordViewSet, PolicyCheckRunViewSet, SecurityIncidentViewSet

router = DefaultRouter()
router.register('data-processing', DataProcessingRecordViewSet)
router.register('consents', ConsentRecordViewSet)
router.register('incidents', SecurityIncidentViewSet)
router.register('checks', PolicyCheckRunViewSet)
urlpatterns = [path('', include(router.urls))]
