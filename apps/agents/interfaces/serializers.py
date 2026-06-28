from rest_framework import serializers
from apps.agents.infrastructure.models import AgentProfile, AtlasEmailDraft, AtlasProspect, VirtualAssistantMessage, VirtualAssistantSession

class AgentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentProfile
        fields = '__all__'

class VirtualAssistantSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualAssistantSession
        fields = '__all__'

class VirtualAssistantMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualAssistantMessage
        fields = '__all__'

class AtlasProspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtlasProspect
        fields = '__all__'

class AtlasEmailDraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtlasEmailDraft
        fields = '__all__'
