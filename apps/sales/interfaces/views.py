from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.sales.infrastructure.models import SalesOrder, SalesOrderItem
from apps.sales.interfaces.serializers import SalesOrderItemSerializer, SalesOrderSerializer

class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.select_related('customer','organization','created_by').prefetch_related('items').all()
    serializer_class = SalesOrderSerializer
    search_fields = ['number','customer__name','notes']
    filterset_fields = ['organization','customer','status']
    ordering_fields = ['created_at','total_amount']

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        order = self.get_object()
        order.status = 'confirmed'
        order.save(update_fields=['status','updated_at'])
        return Response({'success': True, 'data': self.get_serializer(order).data})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        order.status = 'cancelled'
        order.save(update_fields=['status','updated_at'])
        return Response({'success': True, 'data': self.get_serializer(order).data})

class SalesOrderItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SalesOrderItem.objects.select_related('order','product').all()
    serializer_class = SalesOrderItemSerializer
    filterset_fields = ['order','product']
