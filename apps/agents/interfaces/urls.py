from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.agents.interfaces.views import AgentProfileViewSet, AtlasEmailDraftViewSet, AtlasProspectViewSet, VirtualAssistantMessageViewSet, VirtualAssistantSessionViewSet

router = DefaultRouter()
router.register('profiles', AgentProfileViewSet)
router.register('livia/sessions', VirtualAssistantSessionViewSet)
router.register('livia/messages', VirtualAssistantMessageViewSet)
router.register('atlas/prospects', AtlasProspectViewSet)
router.register('atlas/email-drafts', AtlasEmailDraftViewSet)
urlpatterns = [path('', include(router.urls))]
