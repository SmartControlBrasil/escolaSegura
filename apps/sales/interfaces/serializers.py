from rest_framework import serializers
from apps.customers.infrastructure.models import Customer
from apps.sales.application.services import SalesOrderService
from apps.sales.infrastructure.models import SalesOrder, SalesOrderItem

class SalesOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrderItem
        fields = ['id','order','product','description','quantity','unit_price','subtotal','created_at','updated_at']
        read_only_fields = ['id','order','subtotal','created_at','updated_at']

class SalesOrderSerializer(serializers.ModelSerializer):
    items = SalesOrderItemSerializer(many=True, read_only=True)
    input_items = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = SalesOrder
        fields = ['id','organization','customer','number','status','total_amount','notes','created_by','items','input_items','created_at','updated_at']
        read_only_fields = ['id','number','total_amount','created_by','created_at','updated_at']

    def create(self, validated_data):
        items = validated_data.pop('input_items', [])
        request = self.context.get('request')
        user = request.user if request and getattr(request.user, 'is_authenticated', False) else None
        customer = validated_data.pop('customer')
        organization = validated_data.pop('organization', None) or getattr(customer, 'organization', None)
        return SalesOrderService.create_order(customer=customer, organization=organization, created_by=user, items=items, notes=validated_data.get('notes', ''))
