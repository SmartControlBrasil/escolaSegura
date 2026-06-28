from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.core.interfaces.views import ActivityLogViewSet, BranchViewSet, DashboardViewSet, OrganizationViewSet, SystemSettingViewSet

router = DefaultRouter()
router.register('organizations', OrganizationViewSet)
router.register('branches', BranchViewSet)
router.register('settings', SystemSettingViewSet)
router.register('activity-logs', ActivityLogViewSet)
router.register('dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [path('', include(router.urls))]
