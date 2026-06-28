from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.service_reports.interfaces.views import ServiceReportItemViewSet, ServiceReportPhotoViewSet, ServiceReportViewSet

router = DefaultRouter()
router.register('reports', ServiceReportViewSet)
router.register('report-items', ServiceReportItemViewSet)
router.register('report-photos', ServiceReportPhotoViewSet)

urlpatterns = [path('', include(router.urls))]
