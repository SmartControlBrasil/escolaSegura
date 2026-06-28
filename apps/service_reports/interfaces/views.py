from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from apps.service_reports.infrastructure.models import ServiceReport, ServiceReportItem, ServiceReportPhoto
from apps.service_reports.interfaces.serializers import ServiceReportItemSerializer, ServiceReportPhotoSerializer, ServiceReportSerializer


class ServiceReportViewSet(viewsets.ModelViewSet):
    queryset = ServiceReport.objects.select_related('customer','organization','estimate','sales_order','created_by').prefetch_related('items','photos').all()
    serializer_class = ServiceReportSerializer
    search_fields = ['number','title','customer__name','technician_name','problem_reported','service_performed']
    filterset_fields = ['organization','customer','estimate','sales_order','status','service_date']
    ordering_fields = ['service_date','created_at','total_amount']

    def perform_create(self, serializer):
        report = serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None)
        report.ensure_number()

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        report = self.get_object()
        report.status = ServiceReport.Status.COMPLETED
        report.finished_at = timezone.now()
        report.save(update_fields=['status','finished_at','updated_at'])
        return Response({'success': True, 'data': self.get_serializer(report).data})


class ServiceReportItemViewSet(viewsets.ModelViewSet):
    queryset = ServiceReportItem.objects.select_related('report').all()
    serializer_class = ServiceReportItemSerializer
    filterset_fields = ['report','is_billable']


class ServiceReportPhotoViewSet(viewsets.ModelViewSet):
    queryset = ServiceReportPhoto.objects.select_related('report','uploaded_by').all()
    serializer_class = ServiceReportPhotoSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    search_fields = ['caption','technical_notes','report__number','report__title']
    filterset_fields = ['report','category']

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user if self.request.user.is_authenticated else None)


@staff_member_required
def service_reports_dashboard(request):
    context = {
        'draft_count': ServiceReport.objects.filter(status=ServiceReport.Status.DRAFT).count(),
        'in_progress_count': ServiceReport.objects.filter(status=ServiceReport.Status.IN_PROGRESS).count(),
        'completed_count': ServiceReport.objects.filter(status=ServiceReport.Status.COMPLETED).count(),
        'recent_reports': ServiceReport.objects.select_related('customer').all()[:12],
    }
    return render(request, 'service_reports/dashboard.html', context)


@staff_member_required
def service_report_detail(request, report_id):
    report = get_object_or_404(ServiceReport.objects.prefetch_related('items','photos'), id=report_id)
    if request.method == 'POST' and request.FILES.get('image'):
        ServiceReportPhoto.objects.create(
            report=report,
            image=request.FILES['image'],
            category=request.POST.get('category') or ServiceReportPhoto.Category.EVIDENCE,
            caption=request.POST.get('caption',''),
            technical_notes=request.POST.get('technical_notes',''),
            uploaded_by=request.user if request.user.is_authenticated else None,
        )
        return redirect('service-report-detail', report_id=report.id)
    return render(request, 'service_reports/detail.html', {'report': report})
