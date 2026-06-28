from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.sales.interfaces.views import SalesOrderItemViewSet, SalesOrderViewSet

router = DefaultRouter()
router.register('orders', SalesOrderViewSet)
router.register('order-items', SalesOrderItemViewSet)
urlpatterns = [path('', include(router.urls))]
