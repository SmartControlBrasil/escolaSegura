from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.estimates.interfaces.views import (
    EstimateContactMessageViewSet,
    EstimateLineViewSet,
    EstimateMeasurementViewSet,
    EstimatePhotoViewSet,
    EstimateViewSet,
)

router = DefaultRouter()
router.register('estimates', EstimateViewSet)
router.register('estimate-lines', EstimateLineViewSet)
router.register('estimate-photos', EstimatePhotoViewSet)
router.register('estimate-measurements', EstimateMeasurementViewSet)
router.register('estimate-contact-messages', EstimateContactMessageViewSet)

urlpatterns = [path('', include(router.urls))]
