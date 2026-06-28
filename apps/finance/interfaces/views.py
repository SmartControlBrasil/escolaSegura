from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.finance.infrastructure.models import AccountPayable, AccountReceivable
from apps.finance.interfaces.serializers import AccountPayableSerializer, AccountReceivableSerializer

class AccountReceivableViewSet(viewsets.ModelViewSet):
    queryset = AccountReceivable.objects.select_related('customer','organization').all()
    serializer_class = AccountReceivableSerializer
    search_fields = ['description','reference','customer__name']
    filterset_fields = ['organization','customer','status','due_date']

    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        item = self.get_object()
        item.status = 'paid'
        item.paid_at = timezone.now()
        item.save(update_fields=['status','paid_at','updated_at'])
        return Response({'success': True, 'data': self.get_serializer(item).data})

class AccountPayableViewSet(viewsets.ModelViewSet):
    queryset = AccountPayable.objects.select_related('organization').all()
    serializer_class = AccountPayableSerializer
    search_fields = ['description','reference','supplier_name']
    filterset_fields = ['organization','status','due_date']

    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        item = self.get_object()
        item.status = 'paid'
        item.paid_at = timezone.now()
        item.save(update_fields=['status','paid_at','updated_at'])
        return Response({'success': True, 'data': self.get_serializer(item).data})
