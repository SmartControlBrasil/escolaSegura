from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum, Count
from django.utils import timezone
from decimal import Decimal

from apps.customers.infrastructure.models import Customer
from apps.catalog.infrastructure.models import Product
from apps.estimates.infrastructure.models import Estimate, EstimateLine
from apps.service_reports.infrastructure.models import ServiceReport
from apps.agents.infrastructure.models import AtlasProspect, VirtualAssistantSession
from apps.core.infrastructure.models import Organization

@login_required
def dashboard(request):
    # Dynamic values from Database
    total_customers = Customer.objects.count()
    total_estimates = Estimate.objects.count()
    estimates_approved = Estimate.objects.filter(status='approved').count()
    estimates_open = Estimate.objects.filter(status__in=['draft', 'pricing', 'sent']).count()
    
    # 8 commercial cards requested:
    # 1. Leads do mês (mock)
    leads_month = 28
    # 2. Orçamentos abertos
    # 3. Orçamentos aprovados
    # 4. Obras em andamento (mock)
    works_in_progress = 5
    # 5. Vistorias agendadas (estimates with a scheduled visit date in the future)
    scheduled_inspections = Estimate.objects.filter(visit_scheduled_at__gt=timezone.now()).count()
    # 6. Faturamento estimado (sum of approved estimates)
    estimated_revenue = Estimate.objects.filter(status='approved').aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
    # 7. Taxa de conversão
    if total_estimates > 0:
        conversion_rate = (estimates_approved / total_estimates) * 100
    else:
        conversion_rate = 0.0
    # 8. Pendências operacionais (mock)
    operational_issues = 3

    context = {
        'leads_month': leads_month,
        'estimates_open': estimates_open,
        'estimates_approved': estimates_approved,
        'works_in_progress': works_in_progress,
        'scheduled_inspections': scheduled_inspections,
        'estimated_revenue': estimated_revenue,
        'conversion_rate': conversion_rate,
        'operational_issues': operational_issues,
        'total_customers': total_customers,
        'total_estimates': total_estimates,
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
def orcamentos_novo(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        title = request.POST.get('title')
        service_location = request.POST.get('service_location', '')
        scope_summary = request.POST.get('scope_summary', '')
        
        customer = Customer.objects.filter(id=customer_id).first()
        org = Organization.objects.first()
        
        if customer and title:
            est = Estimate.objects.create(
                organization=org,
                customer=customer,
                title=title,
                status='draft',
                service_location=service_location,
                scope_summary=scope_summary,
                created_by=request.user
            )
            est.ensure_number()
            # Add a default line to make it demoable
            product = Product.objects.filter(type='product').first()
            if product:
                EstimateLine.objects.create(
                    estimate=est,
                    product=product,
                    kind='product',
                    description=f'Fornecimento de {product.name}',
                    quantity=Decimal('5.00'),
                    unit_price=product.sale_price
                )
            return redirect('backoffice:orcamentos')
            
    customers_list = Customer.objects.all()
    context = {
        'customers': customers_list
    }
    return render(request, 'backoffice/orcamentos_novo.html', context)

@login_required
def vistorias(request):
    reports_list = ServiceReport.objects.all().order_by('-service_date')
    context = {
        'reports': reports_list
    }
    return render(request, 'backoffice/vistorias.html', context)

@login_required
def relatorios(request):
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

@login_required
def redes_sociais(request):
    # Mocked data for social media posts
    posts = [
        {
            'channel': 'Instagram',
            'suggested_title': 'Elegância em Mármore Carrara',
            'caption': 'Transforme seu banheiro em uma verdadeira suíte de luxo. Bancadas e nichos sob medida em Mármore Carrara. Peça seu orçamento hoje! #carrara #marmoraria #decor',
            'status': 'Agendado'
        },
        {
            'channel': 'Facebook',
            'suggested_title': 'Cozinhas Modernas em Silestone',
            'caption': 'Durabilidade, higiene e design impecável. O Silestone Cinza Expo é perfeito para a bancada da sua cozinha. Fale conosco e conheça as opções!',
            'status': 'Revisão'
        },
        {
            'channel': 'Pinterest',
            'suggested_title': 'Inspiração: Área Gourmet com Granito',
            'caption': 'Ideia fantástica de churrasqueira e varanda gourmet revestidas em Granito Preto São Gabriel Escovado. Lindo e resistente.',
            'status': 'Rascunho'
        }
    ]
    context = {
        'posts': posts
    }
    return render(request, 'backoffice/redes_sociais.html', context)

@login_required
def growth(request):
    # Mock pipeline stages for growth engine
    opportunities = [
        {'client': 'Construtora Liderança', 'project': 'Soleiras Edifício Horizon', 'value': 28500.00, 'stage': 'Negociação'},
        {'client': 'Renata Decor Interiores', 'project': 'Apartamento Higienópolis', 'value': 14200.00, 'stage': 'Proposta Enviada'},
        {'client': 'Carlos Alberto Pf', 'project': 'Escada Social Travertino', 'value': 9800.00, 'stage': 'Qualificação'},
        {'client': 'Clínica Odonto Prime', 'project': 'Recepção Quartzo Branco', 'value': 12000.00, 'stage': 'Fechamento'}
    ]
    context = {
        'opportunities': opportunities
    }
    return render(request, 'backoffice/growth.html', context)

@login_required
def atlas(request):
    # Get prospects that need human review (seeded from Atlas)
    prospects = AtlasProspect.objects.filter(status='review').order_by('-score')
    context = {
        'prospects': prospects
    }
    return render(request, 'backoffice/atlas.html', context)

@login_required
def assistente(request):
    # VA sessions
    sessions = VirtualAssistantSession.objects.all().order_by('-created_at')
    context = {
        'sessions': sessions
    }
    return render(request, 'backoffice/assistente.html', context)

@login_required
def configuracoes(request):
    org = Organization.objects.first()
    context = {
        'organization': org
    }
    return render(request, 'backoffice/configuracoes.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('backoffice:dashboard')
        
    next_url = request.GET.get('next', request.POST.get('next', ''))
    errors = []
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if next_url:
                return redirect(next_url)
            return redirect('backoffice:dashboard')
        else:
            errors = ["Usuário ou senha incorretos."]
            
    context = {
        'errors': errors,
        'next': next_url
    }
    return render(request, 'backoffice/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('backoffice:login')
