from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.inventory.interfaces.views import StockBalanceViewSet, StockLocationViewSet, StockMovementViewSet

router = DefaultRouter()
router.register('locations', StockLocationViewSet)
router.register('balances', StockBalanceViewSet)
router.register('movements', StockMovementViewSet)
urlpatterns = [path('', include(router.urls))]
