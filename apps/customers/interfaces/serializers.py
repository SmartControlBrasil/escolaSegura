from rest_framework import serializers
from apps.customers.infrastructure.models import Customer, CustomerAddress, CustomerContact

class CustomerContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerContact
        fields = ['id','customer','name','role','email','phone','is_primary','created_at','updated_at']
        read_only_fields = ['id','created_at','updated_at']

class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = ['id','customer','label','street','number','complement','district','city','state','zipcode','created_at','updated_at']
        read_only_fields = ['id','created_at','updated_at']

class CustomerSerializer(serializers.ModelSerializer):
    contacts = CustomerContactSerializer(many=True, read_only=True)
    addresses = CustomerAddressSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ['id','organization','type','name','legal_name','document','email','phone','city','state','status','notes','contacts','addresses','created_at','updated_at']
        read_only_fields = ['id','created_at','updated_at']
