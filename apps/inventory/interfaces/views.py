from rest_framework import viewsets
from apps.inventory.infrastructure.models import StockBalance, StockLocation, StockMovement
from apps.inventory.interfaces.serializers import StockBalanceSerializer, StockLocationSerializer, StockMovementSerializer

class StockLocationViewSet(viewsets.ModelViewSet):
    queryset = StockLocation.objects.all()
    serializer_class = StockLocationSerializer
    search_fields = ['name','code']
    filterset_fields = ['organization','is_active']

class StockBalanceViewSet(viewsets.ModelViewSet):
    queryset = StockBalance.objects.select_related('product','location').all()
    serializer_class = StockBalanceSerializer
    filterset_fields = ['product','location']

class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.select_related('product','location','created_by').all()
    serializer_class = StockMovementSerializer
    search_fields = ['reason','reference']
    filterset_fields = ['product','location','type']
