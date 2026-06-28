from django.shortcuts import render, redirect, get_object_or_404
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
from apps.core.infrastructure.models import Organization, ActivityLog

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
def clientes_novo(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        document = request.POST.get('document', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        ctype = request.POST.get('type', 'company')
        
        org = Organization.objects.first()
        
        if name:
            c = Customer.objects.create(
                organization=org,
                name=name,
                document=document,
                email=email,
                phone=phone,
                type=ctype
            )
            log_activity(request, request.user, 'customer_created', obj=c)
            return redirect('backoffice:clientes')

    return render(request, 'backoffice/clientes_novo.html')

@login_required
def clientes_detalhe(request, id):
    customer = get_object_or_404(Customer, id=id)
    if request.method == 'POST':
        customer.name = request.POST.get('name', customer.name)
        customer.document = request.POST.get('document', customer.document)
        customer.email = request.POST.get('email', customer.email)
        customer.phone = request.POST.get('phone', customer.phone)
        customer.type = request.POST.get('type', customer.type)
        customer.save()
        log_activity(request, request.user, 'customer_updated', obj=customer)
        return redirect('backoffice:clientes')
        
    context = {'customer': customer}
    return render(request, 'backoffice/clientes_detalhe.html', context)

@login_required
def catalogo(request):
    products_list = Product.objects.all().order_by('category__name', 'name')
    context = {
        'products': products_list
    }
    return render(request, 'backoffice/catalogo.html', context)

@login_required
def catalogo_novo(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        ptype = request.POST.get('type', 'product')
        unit = request.POST.get('unit', 'un')
        sale_price = request.POST.get('sale_price', '0.00')
        
        org = Organization.objects.first()
        
        if name:
            p = Product.objects.create(
                organization=org,
                name=name,
                type=ptype,
                unit=unit,
                sale_price=Decimal(sale_price.replace(',', '.')) if sale_price else Decimal('0.00')
            )
            log_activity(request, request.user, 'product_created', obj=p)
            return redirect('backoffice:catalogo')
            
    return render(request, 'backoffice/catalogo_novo.html')

@login_required
def catalogo_detalhe(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product.name = request.POST.get('name', product.name)
        product.type = request.POST.get('type', product.type)
        product.unit = request.POST.get('unit', product.unit)
        sale_price = request.POST.get('sale_price')
        if sale_price:
            product.sale_price = Decimal(sale_price.replace(',', '.'))
        product.save()
        log_activity(request, request.user, 'product_updated', obj=product)
        return redirect('backoffice:catalogo')
        
    context = {'product': product}
    return render(request, 'backoffice/catalogo_detalhe.html', context)

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
            log_activity(request, request.user, 'estimate_created', obj=est)
            return redirect('backoffice:orcamentos')
            
    customers_list = Customer.objects.all()
    context = {
        'customers': customers_list
    }
    return render(request, 'backoffice/orcamentos_novo.html', context)

@login_required
def orcamentos_detalhe(request, id):
    estimate = get_object_or_404(Estimate, id=id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_status':
            new_status = request.POST.get('status')
            if new_status:
                estimate.status = new_status
                estimate.save()
                log_activity(request, request.user, 'estimate_status_updated', obj=estimate, metadata={'new_status': new_status})
        elif action == 'add_item':
            product_id = request.POST.get('product')
            quantity = request.POST.get('quantity', '1')
            if product_id:
                product = get_object_or_404(Product, id=product_id)
                EstimateLine.objects.create(
                    estimate=estimate,
                    product=product,
                    kind=product.type,
                    description=f'Fornecimento de {product.name}',
                    unit=product.unit,
                    quantity=Decimal(quantity.replace(',', '.')),
                    unit_price=product.sale_price
                )
                log_activity(request, request.user, 'estimate_item_added', obj=estimate)
        elif action == 'remove_item':
            line_id = request.POST.get('line_id')
            if line_id:
                EstimateLine.objects.filter(id=line_id, estimate=estimate).delete()
                estimate.recalculate_totals()
                log_activity(request, request.user, 'estimate_item_removed', obj=estimate)
                
        return redirect('backoffice:orcamentos_detalhe', id=id)
        
    products = Product.objects.filter(is_active=True)
    context = {
        'estimate': estimate,
        'products': products
    }
    return render(request, 'backoffice/orcamentos_detalhe.html', context)

@login_required
def orcamentos_preview(request, id):
    estimate = get_object_or_404(Estimate, id=id)
    org = Organization.objects.first()
    context = {
        'estimate': estimate,
        'organization': org
    }
    return render(request, 'backoffice/orcamentos_preview.html', context)

@login_required
def vistorias(request):
    reports_list = ServiceReport.objects.all().order_by('-service_date')
    context = {
        'reports': reports_list
    }
    return render(request, 'backoffice/vistorias.html', context)

@login_required
def vistorias_novo(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        title = request.POST.get('title')
        service_location = request.POST.get('service_location', '')
        
        customer = Customer.objects.filter(id=customer_id).first()
        org = Organization.objects.first()
        
        if customer and title:
            rep = ServiceReport.objects.create(
                organization=org,
                customer=customer,
                title=title,
                status='draft',
                service_location=service_location,
                created_by=request.user
            )
            rep.ensure_number()
            log_activity(request, request.user, 'servicereport_created', obj=rep)
            return redirect('backoffice:vistorias')
            
    customers_list = Customer.objects.all()
    context = {'customers': customers_list}
    return render(request, 'backoffice/vistorias_novo.html', context)

@login_required
def vistorias_detalhe(request, id):
    report = get_object_or_404(ServiceReport, id=id)
    if request.method == 'POST':
        report.title = request.POST.get('title', report.title)
        report.service_location = request.POST.get('service_location', report.service_location)
        report.technician_name = request.POST.get('technician_name', report.technician_name)
        report.status = request.POST.get('status', report.status)
        report.problem_reported = request.POST.get('problem_reported', report.problem_reported)
        report.service_performed = request.POST.get('service_performed', report.service_performed)
        report.save()
        log_activity(request, request.user, 'servicereport_updated', obj=report)
        return redirect('backoffice:vistorias')
        
    context = {'report': report}
    return render(request, 'backoffice/vistorias_detalhe.html', context)

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


def log_activity(request, user, action, obj=None, metadata=None):
    # Try to extract IP address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
        
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    org = user.organization if (user and hasattr(user, 'organization')) else None
    
    ActivityLog.objects.create(
        actor=user if (user and user.is_authenticated) else None,
        organization=org,
        action=action,
        object_type=obj.__class__.__name__ if obj else '',
        object_id=str(obj.id) if obj else '',
        ip_address=ip,
        user_agent=user_agent,
        metadata=metadata or {}
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect('backoffice:dashboard')
        
    next_url = request.GET.get('next', request.POST.get('next', ''))
    errors = []
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:
                login(request, user)
                log_activity(request, user, 'login_success')
                if next_url:
                    return redirect(next_url)
                return redirect('backoffice:dashboard')
            else:
                errors = ["Usuário ou senha incorretos."]
                log_activity(request, None, 'login_failed_inactive', metadata={'username': request.POST.get('username')})
        else:
            errors = ["Usuário ou senha incorretos."]
            log_activity(request, None, 'login_failed', metadata={'username': request.POST.get('username')})
            
    context = {
        'errors': errors,
        'next': next_url
    }
    return render(request, 'backoffice/login.html', context)


def logout_view(request):
    if request.user.is_authenticated:
        log_activity(request, request.user, 'logout')
    logout(request)
    return redirect('backoffice:login')

