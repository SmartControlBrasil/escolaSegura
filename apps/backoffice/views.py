from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count

from apps.customers.infrastructure.models import Customer
from apps.catalog.infrastructure.models import Product
from apps.estimates.infrastructure.models import Estimate
from apps.service_reports.infrastructure.models import ServiceReport

@login_required
def dashboard(request):
    # Stats for the main dashboard
    total_customers = Customer.objects.count()
    total_products = Product.objects.count()
    total_estimates = Estimate.objects.count()
    total_reports = ServiceReport.objects.count()

    estimates_sum = Estimate.objects.aggregate(total=Sum('total_amount'))['total'] or 0.00
    
    context = {
        'total_customers': total_customers,
        'total_products': total_products,
        'total_estimates': total_estimates,
        'total_reports': total_reports,
        'estimates_sum': estimates_sum,
    }
    return render(request, 'backoffice/index.html', context)

@login_required
def clientes(request):
    customers_list = Customer.objects.all().order_by('name')
    context = {
        'customers': customers_list
    }
    return render(request, 'backoffice/clientes.html', context)

@login_required
def catalogo(request):
    products_list = Product.objects.all().order_by('category__name', 'name')
    context = {
        'products': products_list
    }
    return render(request, 'backoffice/catalogo.html', context)

@login_required
def orcamentos(request):
    estimates_list = Estimate.objects.all().order_by('-created_at')
    context = {
        'estimates': estimates_list
    }
    return render(request, 'backoffice/orcamentos.html', context)

@login_required
def vistorias(request):
    reports_list = ServiceReport.objects.all().order_by('-service_date')
    context = {
        'reports': reports_list
    }
    return render(request, 'backoffice/vistorias.html', context)

@login_required
def relatorios(request):
    # Basic report stats
    total_estimates = Estimate.objects.count()
    total_approved = Estimate.objects.filter(status='approved').count()
    total_pending = Estimate.objects.filter(status__in=['draft', 'pricing', 'sent']).count()
    
    estimates_by_status = Estimate.objects.values('status').annotate(count=Count('id'), total=Sum('total_amount'))

    context = {
        'total_estimates': total_estimates,
        'total_approved': total_approved,
        'total_pending': total_pending,
        'estimates_by_status': estimates_by_status,
    }
    return render(request, 'backoffice/relatorios.html', context)
