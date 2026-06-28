from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.policy_guard.application.services import PolicyGuardService
from apps.policy_guard.infrastructure.models import ConsentRecord, DataProcessingRecord, PolicyCheckRun, SecurityIncident
from apps.policy_guard.interfaces.serializers import ConsentRecordSerializer, DataProcessingRecordSerializer, PolicyCheckRunSerializer, SecurityIncidentSerializer

class DataProcessingRecordViewSet(viewsets.ModelViewSet):
    queryset = DataProcessingRecord.objects.all()
    serializer_class = DataProcessingRecordSerializer
    search_fields = ['process_name','legal_basis','purpose','owner']
    filterset_fields = ['legal_basis','is_active']

class ConsentRecordViewSet(viewsets.ModelViewSet):
    queryset = ConsentRecord.objects.all()
    serializer_class = ConsentRecordSerializer
    search_fields = ['subject_email','purpose']
    filterset_fields = ['granted','channel']

class SecurityIncidentViewSet(viewsets.ModelViewSet):
    queryset = SecurityIncident.objects.all()
    serializer_class = SecurityIncidentSerializer
    search_fields = ['title','description']
    filterset_fields = ['severity','status']

class PolicyCheckRunViewSet(viewsets.ModelViewSet):
    queryset = PolicyCheckRun.objects.all()
    serializer_class = PolicyCheckRunSerializer

    @action(detail=False, methods=['post'])
    def run_basic(self, request):
        run = PolicyGuardService.run_basic_check()
        return Response({'success': True, 'data': PolicyCheckRunSerializer(run).data})
