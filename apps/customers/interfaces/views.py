from rest_framework import viewsets
from apps.customers.infrastructure.models import Customer, CustomerAddress, CustomerContact
from apps.customers.interfaces.serializers import CustomerAddressSerializer, CustomerContactSerializer, CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.prefetch_related('contacts','addresses').all()
    serializer_class = CustomerSerializer
    search_fields = ['name','legal_name','document','email','phone','city']
    filterset_fields = ['organization','type','status','state']
    ordering_fields = ['name','created_at','updated_at']

class CustomerContactViewSet(viewsets.ModelViewSet):
    queryset = CustomerContact.objects.select_related('customer').all()
    serializer_class = CustomerContactSerializer
    filterset_fields = ['customer','is_primary']

class CustomerAddressViewSet(viewsets.ModelViewSet):
    queryset = CustomerAddress.objects.select_related('customer').all()
    serializer_class = CustomerAddressSerializer
    filterset_fields = ['customer','state','city']
