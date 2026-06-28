from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.pages.interfaces.views import HtmlPageViewSet

router = DefaultRouter()
router.register('', HtmlPageViewSet)
urlpatterns = [path('', include(router.urls))]
