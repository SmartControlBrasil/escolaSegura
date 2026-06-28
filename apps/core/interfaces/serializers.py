from rest_framework import serializers
from apps.core.infrastructure.models import ActivityLog, Branch, Organization, SystemSetting

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id','name','legal_name','document','email','phone','status','created_at','updated_at']
        read_only_fields = ['id','created_at','updated_at']

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id','organization','name','city','state','is_headquarters','created_at','updated_at']
        read_only_fields = ['id','created_at','updated_at']

class SystemSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSetting
        fields = ['id','key','value','description','is_sensitive','created_at','updated_at']
        read_only_fields = ['id','created_at','updated_at']

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = ['id','actor','organization','action','object_type','object_id','metadata','created_at']
        read_only_fields = fields
