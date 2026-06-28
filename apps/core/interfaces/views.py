from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.catalog.infrastructure.models import Product
from apps.core.infrastructure.models import ActivityLog, Branch, Organization, SystemSetting
from apps.core.interfaces.serializers import ActivityLogSerializer, BranchSerializer, OrganizationSerializer, SystemSettingSerializer
from apps.customers.infrastructure.models import Customer
from apps.finance.infrastructure.models import AccountPayable, AccountReceivable
from apps.sales.infrastructure.models import SalesOrder

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    search_fields = ['name', 'document', 'email']
    ordering_fields = ['name', 'created_at']

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.select_related('organization').all()
    serializer_class = BranchSerializer
    filterset_fields = ['organization', 'state', 'is_headquarters']

class SystemSettingViewSet(viewsets.ModelViewSet):
    queryset = SystemSetting.objects.all()
    serializer_class = SystemSettingSerializer
    permission_classes = [IsAdminUser]
    search_fields = ['key', 'description']

class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityLog.objects.select_related('actor','organization').all()
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['action', 'object_type', 'organization']

class DashboardViewSet(viewsets.ViewSet):
    def list(self, request):
        data = {
            'customers': Customer.objects.count(),
            'products': Product.objects.count(),
            'accounts_receivable_open': AccountReceivable.objects.exclude(status='paid').count(),
            'accounts_payable_open': AccountPayable.objects.exclude(status='paid').count(),
            'sales_orders': SalesOrder.objects.count(),
        }
        return Response({'success': True, 'data': data})
