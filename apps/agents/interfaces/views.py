from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.agents.application.services import AtlasProspectorService, LiviaAssistantService
from apps.agents.infrastructure.models import AgentProfile, AtlasEmailDraft, AtlasProspect, VirtualAssistantMessage, VirtualAssistantSession
from apps.agents.interfaces.serializers import AgentProfileSerializer, AtlasEmailDraftSerializer, AtlasProspectSerializer, VirtualAssistantMessageSerializer, VirtualAssistantSessionSerializer

class AgentProfileViewSet(viewsets.ModelViewSet):
    queryset = AgentProfile.objects.all()
    serializer_class = AgentProfileSerializer
    filterset_fields = ['kind','is_active']

class VirtualAssistantSessionViewSet(viewsets.ModelViewSet):
    queryset = VirtualAssistantSession.objects.all()
    serializer_class = VirtualAssistantSessionSerializer

    @action(detail=True, methods=['get'])
    def next_question(self, request, pk=None):
        return Response({'success': True, 'question': LiviaAssistantService.next_question(self.get_object())})

class VirtualAssistantMessageViewSet(viewsets.ModelViewSet):
    queryset = VirtualAssistantMessage.objects.select_related('session').all()
    serializer_class = VirtualAssistantMessageSerializer
    filterset_fields = ['session','role']

class AtlasProspectViewSet(viewsets.ModelViewSet):
    queryset = AtlasProspect.objects.all()
    serializer_class = AtlasProspectSerializer
    search_fields = ['company_name','website','contact_email','city']
    filterset_fields = ['status','state','source']

class AtlasEmailDraftViewSet(viewsets.ModelViewSet):
    queryset = AtlasEmailDraft.objects.select_related('prospect').all()
    serializer_class = AtlasEmailDraftSerializer
    filterset_fields = ['status','approved_by_human']

    @action(detail=True, methods=['post'])
    def send_approved(self, request, pk=None):
        sent = AtlasProspectorService.send_approved_draft(self.get_object())
        return Response({'success': True, 'sent': sent})
