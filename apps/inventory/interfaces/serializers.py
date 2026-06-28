from rest_framework import serializers
from apps.inventory.infrastructure.models import StockBalance, StockLocation, StockMovement

class StockLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockLocation
        fields = ['id','organization','name','code','is_active','created_at','updated_at']
        read_only_fields = ['id','created_at','updated_at']

class StockBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockBalance
        fields = ['id','product','location','quantity','minimum_quantity','created_at','updated_at']
        read_only_fields = ['id','created_at','updated_at']

class StockMovementSerializer(serializers.ModelSerializer):
    apply_now = serializers.BooleanField(write_only=True, default=True)

    class Meta:
        model = StockMovement
        fields = ['id','product','location','type','quantity','reason','reference','created_by','apply_now','created_at','updated_at']
        read_only_fields = ['id','created_by','created_at','updated_at']

    def create(self, validated_data):
        apply_now = validated_data.pop('apply_now', True)
        user = self.context['request'].user if 'request' in self.context else None
        movement = StockMovement(created_by=user if getattr(user, 'is_authenticated', False) else None, **validated_data)
        if apply_now:
            return movement.apply()
        movement.full_clean()
        movement.save()
        return movement
