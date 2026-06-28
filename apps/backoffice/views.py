from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum, Count
from django.utils import timezone
from decimal import Decimal

from apps.customers.infrastructure.models import Customer
from apps.catalog.infrastructure.models import Product
from apps.estimates.infrastructure.models import Estimate, EstimateLine
from apps.core.infrastructure.models import Organization, ActivityLog, Supplier, Vehicle
from apps.sales.infrastructure.models import Project
from apps.service_reports.infrastructure.models import ServiceReport, ProjectDelivery
from apps.finance.infrastructure.models import AccountReceivable, AccountPayable
from apps.accounts.infrastructure.models import User
from apps.agents.infrastructure.models import AtlasProspect, VirtualAssistantSession

from django.template.loader import render_to_string
import weasyprint

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
        whatsapp = request.POST.get('whatsapp', '')
        address = request.POST.get('address', '')
        lead_origin = request.POST.get('lead_origin', '')
        lgpd_consent = request.POST.get('lgpd_consent') == 'on'
        
        org = Organization.objects.first()
        
        if name:
            c = Customer.objects.create(
                organization=org,
                name=name,
                document=document,
                email=email,
                phone=phone,
                type=ctype,
                whatsapp=whatsapp,
                address=address,
                lead_origin=lead_origin,
                lgpd_consent=lgpd_consent
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
        customer.whatsapp = request.POST.get('whatsapp', customer.whatsapp)
        customer.type = request.POST.get('type', customer.type)
        customer.address = request.POST.get('address', customer.address)
        customer.lead_origin = request.POST.get('lead_origin', customer.lead_origin)
        customer.status = request.POST.get('status', customer.status)
        customer.lgpd_consent = request.POST.get('lgpd_consent') == 'on'
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
        
        cost_price = request.POST.get('cost_price', '0.00')
        suggested_margin = request.POST.get('suggested_margin', '0.00')
        supplier_id = request.POST.get('supplier')
        
        org = Organization.objects.first()
        
        if name:
            sup = Supplier.objects.filter(id=supplier_id).first() if supplier_id else None
            p = Product.objects.create(
                organization=org,
                name=name,
                type=ptype,
                unit=unit,
                cost_price=Decimal(cost_price.replace(',', '.')) if cost_price else Decimal('0.00'),
                suggested_margin=Decimal(suggested_margin.replace(',', '.')) if suggested_margin else Decimal('0.00'),
                sale_price=Decimal(sale_price.replace(',', '.')) if sale_price else Decimal('0.00'),
                supplier=sup
            )
            if 'image' in request.FILES:
                p.image = request.FILES['image']
                p.save()
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
        cost_price = request.POST.get('cost_price')
        if cost_price:
            product.cost_price = Decimal(cost_price.replace(',', '.'))
        suggested_margin = request.POST.get('suggested_margin')
        if suggested_margin:
            product.suggested_margin = Decimal(suggested_margin.replace(',', '.'))
            
        supplier_id = request.POST.get('supplier')
        if supplier_id:
            product.supplier_id = supplier_id
            
        product.is_active = request.POST.get('is_active') == 'on'
        
        if 'image' in request.FILES:
            product.image = request.FILES['image']
            
        product.save()
        log_activity(request, request.user, 'product_updated', obj=product)
        return redirect('backoffice:catalogo')
        
    context = {'product': product, 'suppliers': Supplier.objects.all()}
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
        
        if not action:
            # Updating basic info
            estimate.environment = request.POST.get('environment', estimate.environment)
            deadline_days = request.POST.get('deadline_days')
            if deadline_days and deadline_days.isdigit():
                estimate.deadline_days = int(deadline_days)
            validity_days = request.POST.get('validity_days')
            if validity_days and validity_days.isdigit():
                estimate.validity_days = int(validity_days)
            
            discount_amount = request.POST.get('discount_amount')
            if discount_amount:
                estimate.discount_amount = Decimal(discount_amount.replace(',', '.'))
                
            estimate.title = request.POST.get('title', estimate.title)
            estimate.service_location = request.POST.get('service_location', estimate.service_location)
            estimate.terms_and_conditions = request.POST.get('terms_and_conditions', estimate.terms_and_conditions)
            estimate.internal_notes = request.POST.get('internal_notes', estimate.internal_notes)
            estimate.save()
            estimate.recalculate_totals() # recalculate just in case discount changed
            log_activity(request, request.user, 'estimate_updated', obj=estimate)

        elif action == 'update_status':
            new_status = request.POST.get('status')
            if new_status:
                estimate.status = new_status
                estimate.save()
                log_activity(request, request.user, 'estimate_status_updated', obj=estimate, metadata={'new_status': new_status})
        elif action == 'add_item':
            product_id = request.POST.get('product')
            quantity = request.POST.get('quantity', '1')
            length = request.POST.get('length', '0')
            width = request.POST.get('width', '0')
            discount = request.POST.get('discount_amount', '0')
            
            if product_id:
                product = get_object_or_404(Product, id=product_id)
                EstimateLine.objects.create(
                    estimate=estimate,
                    product=product,
                    kind=product.type,
                    description=f'Fornecimento de {product.name}',
                    unit=product.unit,
                    quantity=Decimal(quantity.replace(',', '.') or '0'),
                    length=Decimal(length.replace(',', '.') or '0'),
                    width=Decimal(width.replace(',', '.') or '0'),
                    discount_amount=Decimal(discount.replace(',', '.') or '0'),
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
def orcamentos_pdf(request, id):
    estimate = get_object_or_404(Estimate, id=id)
    org = Organization.objects.first()
    context = {
        'estimate': estimate,
        'organization': org
    }
    
    html_string = render_to_string('backoffice/orcamentos_preview.html', context)
    pdf_file = weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
    
    log_activity(request, request.user, 'estimate_pdf_generated', obj=estimate)
    
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Orcamento_{estimate.number}.pdf"'
    return response

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
        
        scheduled_date = request.POST.get('scheduled_date')
        
        if customer and title:
            rep = ServiceReport.objects.create(
                organization=org,
                customer=customer,
                title=title,
                status='draft',
                service_location=service_location,
                scheduled_date=scheduled_date if scheduled_date else None,
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
        report.risks_reported = request.POST.get('risks_reported', report.risks_reported)
        
        scheduled_date = request.POST.get('scheduled_date')
        if scheduled_date:
            report.scheduled_date = scheduled_date
            
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



# ==========================================
# ENTREGAS DE OBRA
# ==========================================
@login_required
def entregas(request):
    deliveries = ProjectDelivery.objects.all()
    return render(request, 'backoffice/entregas.html', {'deliveries': deliveries})

@login_required
def entregas_novo(request):
    if request.method == 'POST':
        c_id = request.POST.get('customer')
        p_id = request.POST.get('project')
        org = Organization.objects.first()
        if c_id:
            c = Customer.objects.get(id=c_id)
            proj = Project.objects.filter(id=p_id).first() if p_id else None
            d = ProjectDelivery.objects.create(
                organization=org,
                customer=c,
                project=proj,
                notes=request.POST.get('notes', '')
            )
            log_activity(request, request.user, 'delivery_created', obj=d)
            return redirect('backoffice:entregas')
    return render(request, 'backoffice/entregas_novo.html', {
        'customers': Customer.objects.all(),
        'projects': Project.objects.all()
    })

@login_required
def entregas_detalhe(request, id):
    delivery = get_object_or_404(ProjectDelivery, id=id)
    if request.method == 'POST':
        delivery.checklist_completed = request.POST.get('checklist_completed') == 'on'
        delivery.chk_parts_installed = request.POST.get('chk_parts_installed') == 'on'
        delivery.chk_finish_checked = request.POST.get('chk_finish_checked') == 'on'
        delivery.chk_cleaning_done = request.POST.get('chk_cleaning_done') == 'on'
        delivery.chk_customer_oriented = request.POST.get('chk_customer_oriented') == 'on'
        
        delivery.customer_accepted = request.POST.get('customer_accepted') == 'on'
        delivery.pending_issues = request.POST.get('pending_issues', delivery.pending_issues)
        delivery.notes = request.POST.get('notes', delivery.notes)
        delivery.status = request.POST.get('status', delivery.status)
        delivery.save()
        log_activity(request, request.user, 'delivery_updated', obj=delivery)
        return redirect('backoffice:entregas')
    return render(request, 'backoffice/entregas_detalhe.html', {'delivery': delivery})

@login_required
def entregas_preview(request, id):
    delivery = get_object_or_404(ProjectDelivery, id=id)
    org = Organization.objects.first()
    context = {
        'delivery': delivery,
        'organization': org
    }
    return render(request, 'backoffice/entregas_preview.html', context)

@login_required
def entregas_pdf(request, id):
    delivery = get_object_or_404(ProjectDelivery, id=id)
    org = Organization.objects.first()
    context = {
        'delivery': delivery,
        'organization': org
    }
    
    html_string = render_to_string('backoffice/entregas_preview.html', context)
    pdf_file = weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
    
    log_activity(request, request.user, 'delivery_pdf_generated', obj=delivery)
    
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Relatorio_Entrega_{delivery.id}.pdf"'
    return response

# ==========================================
# OBRAS / PROJETOS
# ==========================================
@login_required
def obras(request):
    projects = Project.objects.all()
    return render(request, 'backoffice/obras.html', {'projects': projects})

@login_required
def obras_novo(request):
    if request.method == 'POST':
        c_id = request.POST.get('customer')
        e_id = request.POST.get('estimate')
        org = Organization.objects.first()
        if c_id:
            c = Customer.objects.get(id=c_id)
            est = Estimate.objects.filter(id=e_id).first() if e_id else None
            p = Project.objects.create(
                organization=org,
                customer=c,
                estimate=est,
                title=request.POST.get('title', 'Nova Obra'),
                address=request.POST.get('address', ''),
                notes=request.POST.get('notes', '')
            )
            log_activity(request, request.user, 'project_created', obj=p)
            return redirect('backoffice:obras')
    return render(request, 'backoffice/obras_novo.html', {
        'customers': Customer.objects.all(),
        'estimates': Estimate.objects.filter(status='approved')
    })

@login_required
def obras_detalhe(request, id):
    project = get_object_or_404(Project, id=id)
    if request.method == 'POST':
        project.title = request.POST.get('title', project.title)
        project.address = request.POST.get('address', project.address)
        project.status = request.POST.get('status', project.status)
        project.notes = request.POST.get('notes', project.notes)
        if request.POST.get('scheduled_date'):
            project.scheduled_date = request.POST.get('scheduled_date')
        project.save()
        log_activity(request, request.user, 'project_updated', obj=project)
        return redirect('backoffice:obras')
    return render(request, 'backoffice/obras_detalhe.html', {'project': project})

# ==========================================
# VEÍCULOS
# ==========================================
@login_required
def veiculos(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'backoffice/veiculos.html', {'vehicles': vehicles})

@login_required
def veiculos_novo(request):
    if request.method == 'POST':
        org = Organization.objects.first()
        plate = request.POST.get('plate')
        if plate:
            v = Vehicle.objects.create(
                organization=org,
                plate=plate,
                model=request.POST.get('model', ''),
                brand=request.POST.get('brand', ''),
                usage=request.POST.get('usage', '')
            )
            log_activity(request, request.user, 'vehicle_created', obj=v)
            return redirect('backoffice:veiculos')
    return render(request, 'backoffice/veiculos_novo.html')

@login_required
def veiculos_detalhe(request, id):
    vehicle = get_object_or_404(Vehicle, id=id)
    if request.method == 'POST':
        vehicle.plate = request.POST.get('plate', vehicle.plate)
        vehicle.model = request.POST.get('model', vehicle.model)
        vehicle.brand = request.POST.get('brand', vehicle.brand)
        vehicle.status = request.POST.get('status', vehicle.status)
        vehicle.usage = request.POST.get('usage', vehicle.usage)
        vehicle.notes = request.POST.get('notes', vehicle.notes)
        vehicle.save()
        log_activity(request, request.user, 'vehicle_updated', obj=vehicle)
        return redirect('backoffice:veiculos')
    return render(request, 'backoffice/veiculos_detalhe.html', {'vehicle': vehicle})

# ==========================================
# FORNECEDORES
# ==========================================
@login_required
def fornecedores(request):
    suppliers = Supplier.objects.all()
    return render(request, 'backoffice/fornecedores.html', {'suppliers': suppliers})

@login_required
def fornecedores_novo(request):
    if request.method == 'POST':
        org = Organization.objects.first()
        name = request.POST.get('name')
        if name:
            s = Supplier.objects.create(
                organization=org,
                name=name,
                cnpj=request.POST.get('cnpj', ''),
                phone=request.POST.get('phone', ''),
                email=request.POST.get('email', ''),
                city=request.POST.get('city', ''),
                address=request.POST.get('address', ''),
                category=request.POST.get('category', '')
            )
            log_activity(request, request.user, 'supplier_created', obj=s)
            return redirect('backoffice:fornecedores')
    return render(request, 'backoffice/fornecedores_novo.html')

@login_required
def fornecedores_detalhe(request, id):
    supplier = get_object_or_404(Supplier, id=id)
    if request.method == 'POST':
        supplier.name = request.POST.get('name', supplier.name)
        supplier.cnpj = request.POST.get('cnpj', supplier.cnpj)
        supplier.phone = request.POST.get('phone', supplier.phone)
        supplier.email = request.POST.get('email', supplier.email)
        supplier.city = request.POST.get('city', supplier.city)
        supplier.address = request.POST.get('address', supplier.address)
        supplier.category = request.POST.get('category', supplier.category)
        supplier.is_active = request.POST.get('is_active') == 'on'
        supplier.notes = request.POST.get('notes', supplier.notes)
        supplier.save()
        log_activity(request, request.user, 'supplier_updated', obj=supplier)
        return redirect('backoffice:fornecedores')
    return render(request, 'backoffice/fornecedores_detalhe.html', {'supplier': supplier})

# ==========================================
# FINANCEIRO
# ==========================================
@login_required
def financeiro(request):
    payables = AccountPayable.objects.all()
    receivables = AccountReceivable.objects.all()
    return render(request, 'backoffice/financeiro.html', {
        'payables': payables,
        'receivables': receivables
    })

@login_required
def financeiro_novo(request):
    if request.method == 'POST':
        org = Organization.objects.first()
        ftype = request.POST.get('type')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        due_date = request.POST.get('due_date')

        if description and amount and due_date:
            if ftype == 'payable':
                AccountPayable.objects.create(
                    organization=org,
                    description=description,
                    amount=amount,
                    due_date=due_date
                )
            else:
                c_id = request.POST.get('customer')
                c = Customer.objects.filter(id=c_id).first() if c_id else None
                AccountReceivable.objects.create(
                    organization=org,
                    customer=c,
                    description=description,
                    amount=amount,
                    due_date=due_date
                )
            return redirect('backoffice:financeiro')
    return render(request, 'backoffice/financeiro_novo.html', {'customers': Customer.objects.all()})

@login_required
def financeiro_detalhe(request, id):
    # try payable first
    payable = AccountPayable.objects.filter(id=id).first()
    receivable = None
    if not payable:
        receivable = get_object_or_404(AccountReceivable, id=id)

    if request.method == 'POST':
        status = request.POST.get('status')
        if payable:
            payable.status = status
            if status == 'paid' and not payable.paid_at:
                payable.paid_at = timezone.now()
            payable.save()
        else:
            receivable.status = status
            if status == 'paid' and not receivable.paid_at:
                receivable.paid_at = timezone.now()
            receivable.save()
        return redirect('backoffice:financeiro')

    return render(request, 'backoffice/financeiro_detalhe.html', {
        'item': payable or receivable,
        'type': 'payable' if payable else 'receivable'
    })

# ==========================================
# USUÁRIOS
# ==========================================
from django.contrib.auth.models import Group

@login_required
def usuarios(request):
    users = User.objects.all()
    return render(request, 'backoffice/usuarios.html', {'users': users})

@login_required
def usuarios_novo(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role')
        group_id = request.POST.get('group')
        
        if username and email:
            u = User.objects.create_user(username=username, email=email, password='changeme123')
            u.role = role
            u.save()
            if group_id:
                g = Group.objects.filter(id=group_id).first()
                if g:
                    u.groups.add(g)
            log_activity(request, request.user, 'user_created', obj=u)
            return redirect('backoffice:usuarios')
            
    return render(request, 'backoffice/usuarios_novo.html', {
        'groups': Group.objects.all(),
        'roles': User.Role.choices
    })

@login_required
def usuarios_detalhe(request, id):
    u = get_object_or_404(User, id=id)
    if request.method == 'POST':
        u.first_name = request.POST.get('first_name', u.first_name)
        u.last_name = request.POST.get('last_name', u.last_name)
        u.is_active = request.POST.get('is_active') == 'on'
        u.role = request.POST.get('role', u.role)
        u.save()

        group_id = request.POST.get('group')
        if group_id:
            g = Group.objects.filter(id=group_id).first()
            if g:
                u.groups.clear()
                u.groups.add(g)

        log_activity(request, request.user, 'user_updated', obj=u)
        return redirect('backoffice:usuarios')
        
    return render(request, 'backoffice/usuarios_detalhe.html', {
        'u': u,
        'groups': Group.objects.all(),
        'roles': User.Role.choices
    })
