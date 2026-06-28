from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.accounts.interfaces.views import MeAPIView, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
urlpatterns = [path('me/', MeAPIView.as_view(), name='me'), path('', include(router.urls))]
