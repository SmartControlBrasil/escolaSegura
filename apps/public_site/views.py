from django.shortcuts import render, redirect
from apps.policy_guard.models import PrivacyConsentLog

EDUMIM_IMG = 'public_site/edumim/images'

HOME_MODULES = [
    {'image': f'{EDUMIM_IMG}/all-img/c1.png', 'tag': 'SaaS', 'title': 'Gestão SaaS Multi-escola'},
    {'image': f'{EDUMIM_IMG}/all-img/c2.png', 'tag': 'Acadêmico', 'title': 'Matrículas e Turmas'},
    {'image': f'{EDUMIM_IMG}/all-img/c3.png', 'tag': 'Acadêmico', 'title': 'Frequência Escolar'},
    {'image': f'{EDUMIM_IMG}/all-img/c4.png', 'tag': 'Acadêmico', 'title': 'Boletim e Avaliações'},
    {'image': f'{EDUMIM_IMG}/all-img/c5.png', 'tag': 'Comunicação', 'title': 'Comunicação com Famílias'},
    {'image': f'{EDUMIM_IMG}/all-img/c6.png', 'tag': 'Família', 'title': 'Portal da Família'},
]

HOME_TOPICS = [
    {'icon': f'{EDUMIM_IMG}/icon/t1.svg', 'title': 'Matrículas'},
    {'icon': f'{EDUMIM_IMG}/icon/t2.svg', 'title': 'Frequência'},
    {'icon': f'{EDUMIM_IMG}/icon/t3.svg', 'title': 'Comunicados'},
    {'icon': f'{EDUMIM_IMG}/icon/t4.svg', 'title': 'Boletim'},
    {'icon': f'{EDUMIM_IMG}/icon/t5.svg', 'title': 'Portal da Família'},
    {'icon': f'{EDUMIM_IMG}/icon/t6.svg', 'title': 'Autorizações'},
    {'icon': f'{EDUMIM_IMG}/icon/t7.svg', 'title': 'Mensagens'},
    {'icon': f'{EDUMIM_IMG}/icon/t8.svg', 'title': 'Segurança de Dados'},
]

HOME_PERSONAS = [
    {'image': f'{EDUMIM_IMG}/all-img/team1.png', 'title': 'Direção e Coordenação', 'subtitle': 'Visão geral da escola', 'href': '/app/'},
    {'image': f'{EDUMIM_IMG}/all-img/team2.png', 'title': 'Secretaria', 'subtitle': 'Matrículas e documentos', 'href': '/app/'},
    {'image': f'{EDUMIM_IMG}/all-img/team3.png', 'title': 'Professores', 'subtitle': 'Turmas, frequência e boletim', 'href': '/app/'},
    {'image': f'{EDUMIM_IMG}/all-img/team4.png', 'title': 'Responsáveis e Alunos', 'subtitle': 'Portal da família', 'href': '/familia/'},
]

HOME_BLOG_POSTS = [
    {'image': f'{EDUMIM_IMG}/all-img/blog-1.png', 'title': 'Comunicação rastreável: por que ela muda a rotina da secretaria'},
    {'image': f'{EDUMIM_IMG}/all-img/blog-2.png', 'title': 'LGPD na prática: o que toda escola precisa saber'},
    {'image': f'{EDUMIM_IMG}/all-img/blog-3.png', 'title': 'Boletim digital: mais transparência para as famílias'},
]


def home(request):
    context = {
        'modules': HOME_MODULES,
        'topics': HOME_TOPICS,
        'personas': HOME_PERSONAS,
        'blog_posts': HOME_BLOG_POSTS,
    }
    return render(request, 'public_site/index.html', context)

def about(request):
    return render(request, 'public_site/about.html')

def services(request):
    return render(request, 'public_site/service-list.html')

def projects(request):
    return render(request, 'public_site/project.html')

def blog(request):
    return render(request, 'public_site/blog-list.html')

def contact(request):
    success = request.GET.get('success', '') == '1'
    if request.method == 'POST':
        full_name = request.POST.get('full-name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        consent = request.POST.get('lgpd_consent') == 'on'
        
        if full_name and email and consent:
            # Extract IP
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            PrivacyConsentLog.objects.create(
                name=full_name,
                email=email,
                phone=phone,
                source='contato',
                consent_text='Li e aceito a Política de Privacidade e autorizo o contato para atendimento da minha solicitação.',
                ip_address=ip,
                user_agent=user_agent
            )
            return redirect('/contato/?success=1')
            
    context = {
        'success': success
    }
    return render(request, 'public_site/contact.html', context)

def privacy(request):
    return render(request, 'public_site/privacy.html')

def terms(request):
    return render(request, 'public_site/terms.html')
