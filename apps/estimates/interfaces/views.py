from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from apps.catalog.infrastructure.models import Product
from apps.estimates.application.services import EstimateService
from apps.estimates.infrastructure.models import Estimate, EstimateContactMessage, EstimateLine, EstimateMeasurement, EstimatePhoto
from apps.estimates.interfaces.serializers import (
    EstimateContactMessageSerializer,
    EstimateLineSerializer,
    EstimateMeasurementSerializer,
    EstimatePhotoSerializer,
    EstimateSerializer,
)


class EstimateViewSet(viewsets.ModelViewSet):
    queryset = Estimate.objects.select_related('customer','organization','created_by','assigned_to').prefetch_related('lines','photos','measurements').all()
    serializer_class = EstimateSerializer
    search_fields = ['number','title','customer__name','scope_summary','service_location']
    filterset_fields = ['organization','customer','status','assigned_to']
    ordering_fields = ['created_at','total_amount','visit_scheduled_at']

    @action(detail=True, methods=['post'])
    def recalculate(self, request, pk=None):
        estimate = self.get_object()
        estimate.recalculate_totals()
        return Response({'success': True, 'data': self.get_serializer(estimate).data})

    @action(detail=True, methods=['post'], url_path='generate-contact-message')
    def generate_contact_message(self, request, pk=None):
        estimate = self.get_object()
        channel = request.data.get('channel', 'whatsapp')
        message = EstimateService.generate_first_contact_message(estimate, channel=channel)
        return Response({'success': True, 'data': EstimateContactMessageSerializer(message, context={'request': request}).data})

    @action(detail=True, methods=['post'], url_path='mark-sent')
    def mark_sent(self, request, pk=None):
        estimate = self.get_object()
        estimate.status = Estimate.Status.SENT
        estimate.save(update_fields=['status','updated_at'])
        return Response({'success': True, 'data': self.get_serializer(estimate).data})


class EstimateLineViewSet(viewsets.ModelViewSet):
    queryset = EstimateLine.objects.select_related('estimate','product').all()
    serializer_class = EstimateLineSerializer
    filterset_fields = ['estimate','product','kind']


class EstimatePhotoViewSet(viewsets.ModelViewSet):
    queryset = EstimatePhoto.objects.select_related('estimate','uploaded_by').all()
    serializer_class = EstimatePhotoSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    search_fields = ['caption','measurement_notes','estimate__number','estimate__title']
    filterset_fields = ['estimate','category']

    def perform_create(self, serializer):
        user = self.request.user if getattr(self.request.user, 'is_authenticated', False) else None
        serializer.save(uploaded_by=user)


class EstimateMeasurementViewSet(viewsets.ModelViewSet):
    queryset = EstimateMeasurement.objects.select_related('estimate').all()
    serializer_class = EstimateMeasurementSerializer
    search_fields = ['label','notes']
    filterset_fields = ['estimate','unit']


class EstimateContactMessageViewSet(viewsets.ModelViewSet):
    queryset = EstimateContactMessage.objects.select_related('estimate').all()
    serializer_class = EstimateContactMessageSerializer
    search_fields = ['subject','body','estimate__number']
    filterset_fields = ['estimate','channel','status','approved_by_human']


@staff_member_required
def estimates_dashboard(request):
    context = {
        'draft_count': Estimate.objects.filter(status=Estimate.Status.DRAFT).count(),
        'inspection_count': Estimate.objects.filter(status=Estimate.Status.INSPECTION).count(),
        'sent_count': Estimate.objects.filter(status=Estimate.Status.SENT).count(),
        'approved_count': Estimate.objects.filter(status=Estimate.Status.APPROVED).count(),
        'recent_estimates': Estimate.objects.select_related('customer').all()[:12],
    }
    return render(request, 'estimates/dashboard.html', context)


@staff_member_required
def estimate_builder(request, estimate_id=None):
    estimate = None
    products = Product.objects.filter(is_active=True).order_by('name')[:200]
    if estimate_id:
        estimate = get_object_or_404(Estimate.objects.prefetch_related('lines','photos','measurements','contact_messages'), id=estimate_id)
        if request.method == 'POST':
            action = request.POST.get('action')
            if action == 'update_estimate':
                estimate.title = request.POST.get('title') or estimate.title
                estimate.service_location = request.POST.get('service_location','')
                estimate.scope_summary = request.POST.get('scope_summary','')
                estimate.customer_message = request.POST.get('customer_message','')
                estimate.terms_and_conditions = request.POST.get('terms_and_conditions','')
                estimate.labor_amount = request.POST.get('labor_amount') or 0
                estimate.discount_amount = request.POST.get('discount_amount') or 0
                estimate.tax_amount = request.POST.get('tax_amount') or 0
                estimate.save()
                estimate.recalculate_totals()
            elif action == 'add_line':
                product = None
                product_id = request.POST.get('product')
                if product_id:
                    product = Product.objects.filter(id=product_id).first()
                EstimateLine.objects.create(
                    estimate=estimate,
                    product=product,
                    kind=request.POST.get('kind') or EstimateLine.Kind.SERVICE,
                    description=request.POST.get('description') or getattr(product, 'name', 'Item do orçamento'),
                    unit=request.POST.get('unit') or getattr(product, 'unit', 'un'),
                    quantity=request.POST.get('quantity') or '1.000',
                    unit_price=request.POST.get('unit_price') or getattr(product, 'sale_price', 0),
                    discount_amount=request.POST.get('discount_amount') or 0,
                    notes=request.POST.get('notes',''),
                )
            elif action == 'generate_contact_message':
                EstimateService.generate_first_contact_message(estimate, channel=request.POST.get('channel','whatsapp'))
            return redirect('estimates-builder-edit', estimate_id=estimate.id)
    elif request.method == 'POST':
        title = request.POST.get('title') or 'Novo orçamento'
        estimate = Estimate.objects.create(title=title, scope_summary=request.POST.get('scope_summary',''), service_location=request.POST.get('service_location',''))
        estimate.ensure_number()
        return redirect('estimates-builder-edit', estimate_id=estimate.id)
    return render(request, 'estimates/builder.html', {'estimate': estimate, 'products': products})


@staff_member_required
def mobile_inspection(request, estimate_id):
    estimate = get_object_or_404(Estimate.objects.prefetch_related('photos','measurements'), id=estimate_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_measurement':
            EstimateMeasurement.objects.create(
                estimate=estimate,
                label=request.POST.get('label') or 'Medida',
                value=request.POST.get('value') or '0',
                unit=request.POST.get('unit') or 'm',
                notes=request.POST.get('notes',''),
            )
        elif request.FILES.get('image'):
            EstimatePhoto.objects.create(
                estimate=estimate,
                image=request.FILES['image'],
                category=request.POST.get('category') or EstimatePhoto.Category.BEFORE,
                caption=request.POST.get('caption',''),
                measurement_notes=request.POST.get('measurement_notes',''),
                uploaded_by=request.user if request.user.is_authenticated else None,
            )
        estimate.status = Estimate.Status.INSPECTION
        estimate.save(update_fields=['status','updated_at'])
        return redirect('estimates-mobile-inspection', estimate_id=estimate.id)
    return render(request, 'estimates/mobile_inspection.html', {'estimate': estimate})
