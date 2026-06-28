from rest_framework import serializers
from apps.finance.infrastructure.models import AccountPayable, AccountReceivable

class AccountReceivableSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountReceivable
        fields = ['id','organization','customer','description','amount','issue_date','due_date','paid_at','status','reference','notes','created_at','updated_at']
        read_only_fields = ['id','created_at','updated_at']

class AccountPayableSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountPayable
        fields = ['id','organization','supplier_name','description','amount','issue_date','due_date','paid_at','status','reference','notes','created_at','updated_at']
        read_only_fields = ['id','created_at','updated_at']
