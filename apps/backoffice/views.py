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
    'dashboard-dark': 'index-2',
    'dashboard-finance': 'finance',
    'alunos-detalhe': 'student-detail',
    'alunos-novo': 'add-student',
    'colaboradores-detalhe': 'teacher-detail',
    'colaboradores-novo': 'add-teacher',
    'autorizacoes': 'form-wizard',
    'comunicados-redigir': 'email-compose',
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
    'unidades': 'Unidades',
    'escolas': 'Unidades',
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

MOCK_MODULES = {
    'dashboard': ('Dashboard', 'Visão geral operacional da Escola Segura', 'Atualizar painel', ['Alunos presentes', 'Responsáveis ativos', 'Acessos hoje', 'Alertas em aberto'], ['Movimento recente', 'Pessoa', 'Tipo', 'Status'], [['07:12', 'Marina Alves', 'Entrada de aluno', 'Liberado'], ['07:18', 'Rafael Costa', 'Responsável autorizado', 'Registrado'], ['08:04', 'Equipe portaria', 'Ronda de pátio', 'Concluído']]),
    'alunos': ('Alunos', 'Cadastro escolar e situação diária dos estudantes', 'Novo aluno', ['Matriculados', 'Presentes hoje', 'Em transporte', 'Aguardando saída'], ['Aluno', 'Turma', 'Responsável', 'Status'], [['Ana Beatriz Lima', '5º A', 'Carla Lima', 'Presente'], ['Pedro Henrique Souza', '7º B', 'Marcos Souza', 'Em aula'], ['Luiza Martins', '3º C', 'Renata Martins', 'Saída autorizada']]),
    'responsaveis': ('Responsáveis', 'Contatos autorizados para retirada, avisos e emergências', 'Novo responsável', ['Responsáveis ativos', 'Com biometria', 'Pendências', 'Bloqueios'], ['Nome', 'Aluno vinculado', 'Documento', 'Autorização'], [['Carla Lima', 'Ana Beatriz Lima', 'CPF validado', 'Retirada e comunicados'], ['Marcos Souza', 'Pedro Henrique Souza', 'CPF validado', 'Retirada'], ['Renata Martins', 'Luiza Martins', 'Documento pendente', 'Comunicados']]),
    'turmas': ('Turmas', 'Organização acadêmica por série, turno e sala', 'Nova turma', ['Turmas ativas', 'Turno manhã', 'Turno tarde', 'Sem sala fixa'], ['Turma', 'Turno', 'Sala', 'Professor referência'], [['5º A', 'Manhã', 'Sala 12', 'Paula Ribeiro'], ['7º B', 'Manhã', 'Sala 18', 'Eduardo Nunes'], ['3º C', 'Tarde', 'Sala 05', 'Mariana Rocha']]),
    'unidades': ('Unidades', 'Campi, prédios e pontos de atendimento do PortalK12', 'Nova unidade', ['Unidades', 'Portarias', 'Câmeras vinculadas', 'Catracas'], ['Unidade', 'Bairro', 'Ponto principal', 'Status'], [['Unidade Centro', 'Centro', 'Portaria A', 'Operando'], ['Unidade Norte', 'Jardim Norte', 'Portaria B', 'Operando'], ['Unidade Infantil', 'Vila Verde', 'Recepção', 'Operando']]),
    'colaboradores': ('Colaboradores', 'Equipe escolar, permissões e vínculos operacionais', 'Novo colaborador', ['Ativos', 'Docentes', 'Operação', 'Acessos suspensos'], ['Nome', 'Área', 'Unidade', 'Status'], [['Paula Ribeiro', 'Pedagógico', 'Unidade Centro', 'Ativa'], ['João Batista', 'Portaria', 'Unidade Norte', 'Ativo'], ['Helena Duarte', 'Cantina', 'Unidade Infantil', 'Ativa']]),
    'visitantes': ('Visitantes', 'Pré-cadastros, check-in e acompanhamento na unidade', 'Registrar visitante', ['Hoje', 'Na unidade', 'Agendados', 'Aguardando saída'], ['Visitante', 'Destino', 'Documento', 'Status'], [['Fernanda Gomes', 'Secretaria', 'RG conferido', 'Na unidade'], ['Carlos Andrade', 'Coordenação', 'CPF conferido', 'Agendado'], ['Marta Silva', 'Financeiro escolar', 'RG conferido', 'Finalizado']]),
    'controle-acesso': ('Controle de Acesso', 'Eventos de entrada, saída e permissões em tempo real', 'Nova autorização', ['Entradas hoje', 'Saídas hoje', 'Alertas', 'Dispositivos online'], ['Horário', 'Pessoa', 'Ponto', 'Resultado'], [['07:05', 'Ana Beatriz Lima', 'Catraca 01', 'Liberado'], ['07:22', 'João Batista', 'Portaria A', 'Liberado'], ['08:11', 'Visitante agendado', 'Recepção', 'Aguardando validação']]),
    'catracas': ('Catracas', 'Monitoramento dos equipamentos de bloqueio e liberação', 'Adicionar dispositivo', ['Online', 'Com alerta', 'Liberações hoje', 'Unidades cobertas'], ['Dispositivo', 'Unidade', 'Último evento', 'Status'], [['Catraca 01', 'Unidade Centro', '07:05', 'Online'], ['Catraca 04', 'Unidade Norte', '07:43', 'Online'], ['Catraca 09', 'Unidade Infantil', '08:02', 'Atenção']]),
    'cameras': ('Câmeras', 'Mapa mockado de vigilância e disponibilidade dos pontos', 'Vincular câmera', ['Câmeras online', 'Gravando', 'Com manutenção', 'Áreas cobertas'], ['Câmera', 'Área', 'Última verificação', 'Status'], [['CAM-PORT-A-01', 'Portaria A', '08:10', 'Online'], ['CAM-PATIO-03', 'Pátio central', '08:09', 'Online'], ['CAM-CANT-02', 'Cantina', '07:58', 'Manutenção programada']]),
    'ocorrencias': ('Ocorrências', 'Registro escolar de segurança, disciplina e atendimento', 'Nova ocorrência', ['Abertas', 'Em análise', 'Resolvidas no mês', 'Com responsável avisado'], ['Data', 'Aluno/Área', 'Categoria', 'Status'], [['Hoje 08:20', 'Pátio central', 'Acompanhamento', 'Em análise'], ['Ontem 15:40', '7º B', 'Orientação pedagógica', 'Responsável avisado'], ['Ontem 10:15', 'Portaria', 'Segurança', 'Resolvida']]),
    'comunicados': ('Comunicados', 'Mensagens institucionais para famílias e equipe escolar', 'Redigir comunicado', ['Enviados no mês', 'Agendados', 'Rascunhos', 'Pendentes'], ['Título', 'Público', 'Canal', 'Status'], [['Reunião pedagógica', 'Responsáveis 5º ano', 'App e e-mail', 'Agendado'], ['Cardápio da semana', 'Toda escola', 'App', 'Enviado'], ['Simulado interno', 'Ensino fundamental', 'App e SMS', 'Rascunho']]),
    'cantina': ('Cantina', 'Cardápio, estoque simples e operação dos intervalos', 'Novo item', ['Itens ativos', 'Pedidos hoje', 'Combos disponíveis', 'Alertas de estoque'], ['Item', 'Categoria', 'Preço', 'Status'], [['Sanduíche natural', 'Lanche', 'R$ 12,00', 'Disponível'], ['Suco integral', 'Bebida', 'R$ 7,00', 'Disponível'], ['Salada de frutas', 'Sobremesa', 'Baixo estoque', 'Atenção']]),
    'pedidos-lanche': ('Pedidos de Lanche', 'Pedidos realizados por responsáveis e alunos autorizados', 'Novo pedido', ['A preparar', 'Entregues hoje', 'Pagos', 'Com restrição'], ['Pedido', 'Aluno', 'Intervalo', 'Status'], [['#L-1028', 'Ana Beatriz Lima', '09:30', 'Em preparo'], ['#L-1029', 'Pedro Henrique Souza', '09:30', 'Pago'], ['#L-1030', 'Luiza Martins', '15:10', 'Aguardando preparo']]),
    'pagamentos': ('Pagamentos', 'Cobranças escolares mockadas e conciliação operacional', 'Registrar pagamento', ['Recebidos no mês', 'Pendentes', 'Em atraso', 'Lanches pagos hoje'], ['Referência', 'Responsável', 'Categoria', 'Status'], [['#P-8451', 'Carla Lima', 'Mensalidade', 'Pago'], ['#P-8452', 'Marcos Souza', 'Cantina', 'Pago'], ['#P-8453', 'Renata Martins', 'Atividade extra', 'Pendente']]),
    'relatorios': ('Relatórios', 'Indicadores escolares e exportações gerenciais mockadas', 'Gerar relatório', ['Relatórios salvos', 'Exportações mês', 'Painéis ativos', 'Pendências'], ['Relatório', 'Periodicidade', 'Última geração', 'Status'], [['Acessos por unidade', 'Diário', 'Hoje 08:00', 'Disponível'], ['Ocorrências por turma', 'Semanal', 'Segunda-feira', 'Disponível'], ['Pedidos de lanche', 'Diário', 'Hoje 07:30', 'Disponível']]),
    'configuracoes': ('Configurações', 'Parâmetros do painel, permissões e preferências da escola', 'Salvar ajustes', ['Perfis de acesso', 'Regras de retirada', 'Integrações mockadas', 'Alertas pendentes'], ['Configuração', 'Escopo', 'Valor mockado', 'Status'], [['Janela de saída', 'Unidade', '15 minutos', 'Ativo'], ['Notificação de atraso', 'Responsáveis', 'App e SMS', 'Ativo'], ['Dupla validação visitante', 'Portaria', 'Obrigatória', 'Ativo']]),
}

STAT_VALUES = ['932', '842', '64', '7']
STAT_ACCENTS = ['std-data', 'teach-data', 'event-data', 'food-data bg-dark']


def _mock_context(page_key):
    title, subtitle, primary_label, stat_labels, columns, rows = MOCK_MODULES[page_key]
    stats = [
        {'label': label, 'value': STAT_VALUES[index], 'accent': STAT_ACCENTS[index]}
        for index, label in enumerate(stat_labels)
    ]
    return {
        'title': title,
        'subtitle': subtitle,
        'primary_label': primary_label,
        'stats': stats,
        'table_title': f'{title} - visão mockada',
        'columns': columns,
        'rows': rows,
    }


def _render_panel_page(request, page_key: str):
    if page_key == 'escolas':
        page_key = 'unidades'
    if page_key in MOCK_MODULES:
        mock = _mock_context(page_key)
        return render(request, 'admin_shell/portalk12/mock_page.html', {
            'panel_page': page_key,
            'page_heading': mock['title'],
            'mock': mock,
        })
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
