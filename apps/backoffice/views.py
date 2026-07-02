from pathlib import Path

from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404
from django.shortcuts import redirect, render


TEMPLATE_DIR = Path(settings.BASE_DIR) / 'templates' / 'admin_shell' / 'portalk12'
AVAILABLE_PAGES = {p.stem for p in TEMPLATE_DIR.glob('*.html')}

PAGE_MAP = {
    'dashboard': 'index',
    'dashboard-dark': 'index-2',
    'dashboard-finance': 'finance',
    'alunos': 'student',
    'alunos-detalhe': 'student-detail',
    'alunos-novo': 'add-student',
    'responsaveis': 'user',
    'turmas': 'table-datatable-basic',
    'escolas': 'table-datatable-basic',
    'colaboradores': 'teacher',
    'colaboradores-detalhe': 'teacher-detail',
    'colaboradores-novo': 'add-teacher',
    'visitantes': 'file-manager',
    'autorizacoes': 'form-wizard',
    'controle-acesso': 'activity',
    'catracas': 'widget-card',
    'cameras': 'app-calender',
    'ocorrencias': 'post-details',
    'comunicados': 'email-inbox',
    'comunicados-redigir': 'email-compose',
    'cantina': 'food',
    'pedidos-lanche': 'food-details',
    'pagamentos': 'finance',
    'relatorios': 'chart-chartjs',
    'configuracoes': 'form-element',
    'perfil': 'app-profile',
    'tabelas': 'table-datatable-basic',
    'formularios': 'form-element',
    'cards': 'ui-card',
    'graficos': 'chart-morris',
    'erro-404': 'page-error-404',
    'erro-500': 'page-error-500',
    'saas-dashboard': 'widget-list',
    'saas-tenants': 'ecom-customers',
    'saas-plans': 'ecom-product-list',
    'saas-subscriptions': 'ecom-product-order',
}


PAGE_HEADINGS = {
    'dashboard': 'Dashboard',
    'dashboard-dark': 'Dashboard Dark',
    'dashboard-finance': 'Finance',
    'alunos': 'Alunos',
    'alunos-detalhe': 'Detalhe do Aluno',
    'alunos-novo': 'Novo Aluno',
    'responsaveis': 'Responsáveis',
    'turmas': 'Turmas',
    'escolas': 'Escolas',
    'colaboradores': 'Colaboradores',
    'colaboradores-detalhe': 'Detalhe do Colaborador',
    'colaboradores-novo': 'Novo Colaborador',
    'visitantes': 'Visitantes',
    'autorizacoes': 'Autorizações',
    'controle-acesso': 'Controle de Acesso',
    'catracas': 'Catracas',
    'cameras': 'Câmeras',
    'ocorrencias': 'Ocorrências',
    'comunicados': 'Comunicados',
    'comunicados-redigir': 'Redigir Comunicado',
    'cantina': 'Cantina',
    'pedidos-lanche': 'Pedidos de Lanche',
    'pagamentos': 'Pagamentos',
    'relatorios': 'Relatórios',
    'configuracoes': 'Configurações',
    'perfil': 'Meu Perfil',
    'tabelas': 'Tabelas',
    'formularios': 'Formulários',
    'cards': 'Cards',
    'graficos': 'Gráficos',
    'erro-404': 'Erro 404',
    'erro-500': 'Erro 500',
    'saas-dashboard': 'SaaS Dashboard',
    'saas-tenants': 'Tenants',
    'saas-plans': 'Planos',
    'saas-subscriptions': 'Assinaturas',
}


def _render_panel_page(request, page_key: str):
    template_name = PAGE_MAP.get(page_key, page_key)
    if template_name not in AVAILABLE_PAGES:
        raise Http404('Página não encontrada no template Akademi convertido.')
    return render(request, f'admin_shell/portalk12/{template_name}.html', {
        'panel_page': page_key,
        'panel_template': template_name,
        'page_heading': PAGE_HEADINGS.get(page_key, page_key.replace('-', ' ').title()),
    })


@login_required
def dashboard(request):
    return _render_panel_page(request, 'dashboard')


@login_required
def dashboard_dark(request):
    return _render_panel_page(request, 'dashboard-dark')


@login_required
def dashboard_finance(request):
    return _render_panel_page(request, 'dashboard-finance')


@login_required
def panel_page(request, page):
    return _render_panel_page(request, page)


@login_required
def template_page(request, page):
    return _render_panel_page(request, page)


@login_required
def legacy_redirect(request):
    return redirect('backoffice:dashboard')


@login_required
def saas_dashboard(request):
    return _render_panel_page(request, 'saas-dashboard')


@login_required
def saas_tenants(request):
    return _render_panel_page(request, 'saas-tenants')


@login_required
def saas_tenant_detail(request, id):
    return _render_panel_page(request, 'saas-tenants')


@login_required
def saas_plans(request):
    return _render_panel_page(request, 'saas-plans')


@login_required
def saas_subscriptions(request):
    return _render_panel_page(request, 'saas-subscriptions')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('backoffice:dashboard')

    next_url = request.GET.get('next', request.POST.get('next', ''))
    errors = []

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid() and form.get_user().is_active:
            login(request, form.get_user())
            return redirect(next_url or 'backoffice:dashboard')
        errors = ['Usuário ou senha incorretos.']
    else:
        form = AuthenticationForm(request)

    return render(request, 'admin_shell/portalk12/page-login.html', {
        'form': form,
        'errors': errors,
        'next': next_url,
    })


def forgot_password(request):
    if 'page-forgot-password' in AVAILABLE_PAGES:
        return render(request, 'admin_shell/portalk12/page-forgot-password.html')
    return redirect('backoffice:login')


def logout_view(request):
    logout(request)
    return redirect('backoffice:login')
