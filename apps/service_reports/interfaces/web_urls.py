from django.urls import path
from apps.service_reports.interfaces.views import service_report_detail, service_reports_dashboard

urlpatterns = [
    path('', service_reports_dashboard, name='service-reports-dashboard'),
    path('<uuid:report_id>/', service_report_detail, name='service-report-detail'),
]
