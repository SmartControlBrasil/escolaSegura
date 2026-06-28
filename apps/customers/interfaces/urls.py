from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.customers.interfaces.views import CustomerAddressViewSet, CustomerContactViewSet, CustomerViewSet

router = DefaultRouter()
router.register('', CustomerViewSet)
router.register('contacts', CustomerContactViewSet)
router.register('addresses', CustomerAddressViewSet)
urlpatterns = [path('', include(router.urls))]
