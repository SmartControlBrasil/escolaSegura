from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.finance.interfaces.views import AccountPayableViewSet, AccountReceivableViewSet

router = DefaultRouter()
router.register('receivables', AccountReceivableViewSet)
router.register('payables', AccountPayableViewSet)
urlpatterns = [path('', include(router.urls))]
