from rest_framework import serializers
from apps.policy_guard.infrastructure.models import ConsentRecord, DataProcessingRecord, PolicyCheckRun, SecurityIncident

class DataProcessingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataProcessingRecord
        fields = '__all__'

class ConsentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsentRecord
        fields = '__all__'

class SecurityIncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityIncident
        fields = '__all__'

class PolicyCheckRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyCheckRun
        fields = '__all__'
