from django.shortcuts import redirect, render
from apps.policy_guard.models import PrivacyConsentLog

EDUMIM_IMG = 'public_site/edumim/images'

HOME_ONE_COURSES = [
    {'image': f'{EDUMIM_IMG}/all-img/c{n}.png', 'tag': tag, 'price': price, 'title': title}
    for n, tag, price, title in [
        (1, 'Gestão Escolar', 'Incluso', 'Fundamentos De Gestão Escolar E Comunicação'),
        (2, 'Secretaria', 'Incluso', 'Rotinas De Matrícula, Documentos E Frequência'),
        (3, 'Pedagógico', 'Incluso', 'Boletim, Avaliações E Acompanhamento De Turmas'),
        (4, 'Segurança', 'Incluso', 'Controle De Acesso E Monitoramento Escolar'),
        (5, 'Famílias', 'Incluso', 'Portal Do Responsável E Autorizações Digitais'),
        (6, 'Cantina', 'Incluso', 'Pedidos De Lanche E Pagamentos Internos'),
        (7, 'Comunicação', 'Incluso', 'Comunicados, Alertas E Mensagens Rastreáveis'),
        (8, 'Relatórios', 'Incluso', 'Indicadores Para Direção E Secretaria'),
        (9, 'Portaria', 'Incluso', 'Visitantes, Prestadores E Entrada/Saída'),
        (10, 'Ocorrências', 'Incluso', 'Registro E Acompanhamento De Incidentes'),
        (11, 'Financeiro', 'Incluso', 'Cobranças Escolares E Conciliação'),
        (12, 'Integrações', 'Incluso', 'Catracas, Câmeras E Sistemas Externos'),
    ]
]

HOME_ONE_TOPICS = [
    {'icon': f'{EDUMIM_IMG}/icon/t{n}.svg', 'title': title, 'count': count}
    for n, title, count in [
        (1, 'Frequência', '12 Módulos'),
        (2, 'Boletim', '8 Módulos'),
        (3, 'Comunicados', '15 Módulos'),
        (4, 'Controle De Acesso', '6 Módulos'),
        (5, 'Portal Da Família', '10 Módulos'),
        (6, 'Cantina', '4 Módulos'),
        (7, 'Relatórios', '9 Módulos'),
        (8, 'Configurações', '5 Módulos'),
    ]
]

HOME_ONE_TEAM = [
    {'image': f'{EDUMIM_IMG}/all-img/team{n}.png', 'name': name, 'role': role}
    for n, name, role in [
        (1, 'Ana Souza', 'Diretora Escolar'),
        (2, 'Carlos Lima', 'Coordenador Pedagógico'),
        (3, 'Mariana Costa', 'Secretária Escolar'),
        (4, 'Roberto Alves', 'Professor'),
    ]
]

HOME_ONE_BLOGS = [
    {'image': f'{EDUMIM_IMG}/all-img/blog-{n}.png', 'title': title, 'date': 'Em Breve'}
    for n, title in [
        (1, 'Educação É Sobre Formar Líderes De Amanhã'),
        (2, 'Comunicação Eficiente Entre Escola E Famílias'),
        (3, 'Como Organizar A Rotina Da Secretaria Escolar'),
    ]
]

HOME_BLOG_POSTS = [
    {'slug': 'school-access-control-best-practices', 'image': f'{EDUMIM_IMG}/all-img/blog-1.png', 'title': 'School Access Control: Best Practices for Daily Operations'},
    {'slug': 'family-communication-that-reduces-incidents', 'image': f'{EDUMIM_IMG}/all-img/blog-2.png', 'title': 'Family Communication That Reduces Incidents and Delays'},
    {'slug': 'canteen-workflow-with-parent-approval', 'image': f'{EDUMIM_IMG}/all-img/blog-3.png', 'title': 'Canteen Workflow With Parent Approval in Real Time'},
]

_BLOG_LIST_THUMBS = ['b-thub-1.png', 'b-thumb-2.png', 'b-thub-3.png']
BLOG_STANDARD_POSTS = [
    {
        'slug': f'analytics-customers-properly-{n}',
        'image': f'{EDUMIM_IMG}/all-img/{thumb}',
        'title': 'Analytics To Help You Understand Your Customers Properly',
        'excerpt': 'There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour.',
        'date': '21 Feb, 22',
        'read_time': '3 Min Read',
        'tag': 'Education',
    }
    for n, thumb in enumerate(_BLOG_LIST_THUMBS, start=1)
]

BLOG_SIDEBAR_RELATED = [
    {'image': f'{EDUMIM_IMG}/all-img/rc-{n}.png', 'title': 'How to Manage Ads For Clients The Right Way'}
    for n in range(1, 4)
]

BLOG_INSTAGRAM_FEED = [f'{EDUMIM_IMG}/all-img/ins-{n}.png' for n in range(1, 7)]

BLOG_POPULAR_TAGS = [
    'Business', 'Education', 'Design', 'Students', 'Teachers',
    'classNameroom', 'Online', 'e-Learning', 'Book',
]

SINGLE_BLOG_DETAIL = {
    'slug': 'analytics-customers-properly-1',
    'hero_image': f'{EDUMIM_IMG}/all-img/b-s-1.png',
    'title': 'Learn At Your Own Pace, with Lifetime Access on Mobile & Desktop',
    'author': 'Edumim',
    'date': '21 Feb, 22',
    'read_time': '3 Min Read',
    'comments_count': '02 Comments',
    'intro': (
        'There are many variations of passages of Lorem Ipsum available, but the majority have suffered '
        'alteration in some form, by injected humour, or randomised words which don’t look even slightly '
        'believable. As students across the globe continue to see their learning plans significantly.'
    ),
    'quote': (
        '“ Education is one of the most powerful aspects of life. Education and learning allow us to make '
        'sense of the world around us, the world inside of us, and where we fit within the world.”'
    ),
    'quote_author': 'Rosalina D. Jackson',
    'section_title': 'Education Is About Academic Excellence And Cultural Diversity Learning Community',
    'gallery': [f'{EDUMIM_IMG}/all-img/b-s-2.png', f'{EDUMIM_IMG}/all-img/b-s-3.png'],
    'tags': ['Business', 'Education', 'Design'],
    'prev_post': {'image': f'{EDUMIM_IMG}/all-img/rc-1.png', 'title': 'How Technology Can Help You Stay Healthy'},
    'next_post': {'image': f'{EDUMIM_IMG}/all-img/rc-3.png', 'title': 'How Technology Can Help You Stay Healthy'},
}

HOME_TWO_CATEGORIES = [
    {'icon': f'{EDUMIM_IMG}/icon/ct1.svg', 'title': 'Educação Infantil', 'count': 12},
    {'icon': f'{EDUMIM_IMG}/icon/ct2.svg', 'title': 'Ensino Fundamental I', 'count': 24},
    {'icon': f'{EDUMIM_IMG}/icon/ct3.svg', 'title': 'Ensino Fundamental II', 'count': 31},
    {'icon': f'{EDUMIM_IMG}/icon/ct4.svg', 'title': 'Ensino Médio', 'count': 18},
    {'icon': f'{EDUMIM_IMG}/icon/ct5.svg', 'title': 'Educação Técnica', 'count': 9},
    {'icon': f'{EDUMIM_IMG}/icon/ct6.svg', 'title': 'EJA', 'count': 6},
]

HOME_TWO_MODULES = [
    {'image': f'{EDUMIM_IMG}/all-img/c1.png', 'title': 'Gestão De Turmas E Frequência'},
    {'image': f'{EDUMIM_IMG}/all-img/c2.png', 'title': 'Boletim E Avaliações Online'},
    {'image': f'{EDUMIM_IMG}/all-img/c3.png', 'title': 'Comunicados E Mensagens'},
    {'image': f'{EDUMIM_IMG}/all-img/c4.png', 'title': 'Controle De Acesso E Catracas'},
    {'image': f'{EDUMIM_IMG}/all-img/c5.png', 'title': 'Cantina E Pedidos De Lanche'},
    {'image': f'{EDUMIM_IMG}/all-img/c6.png', 'title': 'Relatórios Gerenciais'},
]

HOME_TWO_COUNTERS = [
    {'icon': f'{EDUMIM_IMG}/icon/counter-1.svg', 'num': '82k', 'sector': 'Alunos Gerenciados'},
    {'icon': f'{EDUMIM_IMG}/icon/counter-2.svg', 'num': 460, 'sector': 'Turmas Ativas'},
    {'icon': f'{EDUMIM_IMG}/icon/counter-3.svg', 'num': 20, 'sector': 'Escolas Parceiras'},
    {'icon': f'{EDUMIM_IMG}/icon/counter-4.svg', 'num': 200, 'sector': 'Responsáveis Conectados'},
]

HOME_TWO_BRANDS = [f'{EDUMIM_IMG}/all-img/brands/{n}.svg' for n in range(1, 6)]

HOME_TWO_PLANS = [
    {'name': 'Essencial', 'price': 'Grátis', 'highlight': False, 'features': [
        'Cadastro De Alunos E Turmas', 'Comunicados Ilimitados', 'Suporte Por E-mail',
    ]},
    {'name': 'Profissional', 'price': 'R$ 89,69', 'highlight': True, 'features': [
        'Frequência E Boletim Online', 'Portal Da Família Incluso', 'Suporte Prioritário',
    ]},
    {'name': 'Rede De Ensino', 'price': 'R$ 129,69', 'highlight': False, 'features': [
        'Múltiplas Escolas No Mesmo Painel', 'Relatórios Gerenciais Avançados', 'Gerente De Conta Dedicado',
    ]},
]

HOME_TWO_POSTS = [
    {'image': f'{EDUMIM_IMG}/all-img/c1.png', 'title': 'Como Modernizar A Secretaria Escolar'},
    {'image': f'{EDUMIM_IMG}/all-img/c2.png', 'title': 'Comunicação Eficiente Com As Famílias'},
    {'image': f'{EDUMIM_IMG}/all-img/c3.png', 'title': 'Gestão De Frequência Sem Planilhas'},
    {'image': f'{EDUMIM_IMG}/all-img/c4.png', 'title': 'Segurança De Dados Na Escola (LGPD)'},
]

HOME_TWO_INSTAGRAM = [f'{EDUMIM_IMG}/all-img/ins-{n}.png' for n in range(1, 7)]

HOME_THREE_BRANDS = [f'{EDUMIM_IMG}/all-img/brands/b{n}.svg' for n in range(1, 6)]

HOME_THREE_COURSES = [
    {'image': f'{EDUMIM_IMG}/all-img/c{n}.png', 'tag': tag, 'price': price, 'title': title, 'categories': cats}
    for n, tag, price, title, cats in [
        (1, 'Gestão Escolar', 'Incluso', 'Fundamentos De Gestão Escolar E Comunicação', 'marketing design'),
        (2, 'Secretaria', 'Grátis', 'Rotinas De Matrícula, Documentos E Frequência', 'design finance'),
        (3, 'Pedagógico', 'Incluso', 'Boletim, Avaliações E Acompanhamento De Turmas', 'marketing design'),
        (4, 'Segurança', 'Incluso', 'Controle De Acesso E Monitoramento Escolar', 'marketing'),
        (5, 'Famílias', 'Grátis', 'Portal Do Responsável E Autorizações Digitais', 'finance design'),
        (6, 'Cantina', 'Incluso', 'Pedidos De Lanche E Pagamentos Internos', 'design finance'),
    ]
]

HOME_THREE_TEAM = [
    {'image': f'{EDUMIM_IMG}/all-img/team{n}.png', 'name': name, 'role': role}
    for n, name, role in [
        (5, 'Ana Souza', 'Diretora Escolar'),
        (6, 'Carlos Lima', 'Coordenador Pedagógico'),
        (7, 'Mariana Costa', 'Secretária Escolar'),
        (8, 'Roberto Alves', 'Professor'),
    ]
]

HOME_THREE_EVENTS = [
    {'image': f'{EDUMIM_IMG}/all-img/e{n}.png', 'title': title, 'date': date, 'location': location}
    for n, title, date, location in [
        (1, 'Feira De Inovação Escolar 2026', 'Qui, 15 Mai, 2026 14:00', 'São Paulo, SP'),
        (2, 'Workshop De Gestão Pedagógica', 'Sáb, 22 Jun, 2026 09:00', 'Belo Horizonte, MG'),
        (3, 'Encontro De Responsáveis E Escolas', 'Qua, 10 Jul, 2026 19:00', 'Curitiba, PR'),
    ]
]

HOME_THREE_FAQ = [
    'Como funciona a implantação do PortalK12 na minha escola?',
    'Quais perfis de usuário a plataforma suporta?',
    'Os dados das famílias estão protegidos (LGPD)?',
    'Posso integrar catracas e câmeras existentes?',
]

HOME_THREE_TESTIMONIALS = [
    {
        'quote': '“É Realmente A Melhor Solução Para Nossa Escola”',
        'text': 'O PortalK12 simplificou a rotina da secretaria e melhorou a comunicação com as famílias. Hoje temos tudo organizado em um só painel.',
        'name': 'Alfred Helmerich',
        'role': 'Diretor Escolar',
    },
    {
        'quote': '“Comunicação Rápida E Segura Com Os Responsáveis”',
        'text': 'Conseguimos enviar comunicados, autorizações e alertas com histórico rastreável. A equipe ganhou tempo e as famílias também.',
        'name': 'Patricia Mendes',
        'role': 'Coordenadora Pedagógica',
    },
]

INSTRUCTOR_ONE_TESTIMONIALS = [
    {
        'quote': '“It’s Truly The Best Solution For Me”',
        'text': 'There are many variations of passages of Lorem Ipsum available, but the majority have suffered. There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration.',
        'name': 'Alfred Helmerich',
        'role': 'Executive Training Manager',
    },
    {
        'quote': '“It’s Truly The Best Solution For Me”',
        'text': 'There are many variations of passages of Lorem Ipsum available, but the majority have suffered.',
        'name': 'Alfred Helmerich',
        'role': 'Executive Training Manager',
    },
]

INSTRUCTOR_PROFILE = {
    'name': 'Coralina Cloud',
    'short_name': 'Coralina',
    'role': 'UI/UX Designer',
    'image': f'{EDUMIM_IMG}/all-img/single-ins.png',
    'bio_short': 'Professor & Chair of Department of Computer Science at University the where been since 1994. vulput for the pellentesque commodo.',
    'email': 'info@designpixls.com',
    'phone': '8939 2390 3879 29',
    'location': '6/2, Stavello Hall, Sydney',
}

INSTRUCTOR_PROFILE_STATS = [
    {'icon': f'{EDUMIM_IMG}/icon/counter-1.svg', 'num': '82', 'suffix': 'k+', 'label': 'Enrolled Students'},
    {'icon': f'{EDUMIM_IMG}/icon/counter-2.svg', 'num': '460', 'suffix': '+', 'label': 'Academic Programs'},
    {'icon': f'{EDUMIM_IMG}/icon/counter-3.svg', 'num': '20', 'suffix': '+', 'label': 'Certified Students'},
]

INSTRUCTOR_PROFILE_COURSES = [
    {
        'image': f'{EDUMIM_IMG}/all-img/c{n}.png',
        'tag': 'Art & Design',
        'price': '$29.28',
        'title': 'Basic Fundamentals of Interior & Graphics Design',
        'lessons': '2 Lessons',
        'duration': '4h 30m',
        'rating': '4.8',
    }
    for n in range(1, 5)
]

EVENT_LIST_ITEMS = [
    {
        'image': f'{EDUMIM_IMG}/all-img/e{n}.png',
        'title': 'International Art Fair 2022',
        'date': 'Thu, Oct 5, 2023 03:48 PM',
        'location': 'Humberg City, Germany',
    }
    for n in range(1, 10)
]

EVENT_DETAIL = {
    'title': 'Painting Contest 2022',
    'hero_image': f'{EDUMIM_IMG}/all-img/main-event.png',
    'countdown_date': 'Jan 5, 2024 15:37:25',
    'intro': (
        'There are many variations of passages of Lorem Ipsum available, but the majority have suffered '
        'alteration in some form, by injected humour, or randomised words which don\'t look even '
        'slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure '
        'there isn\'t anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators '
        'on the Internet tend to repeat predefined chunks as necessary, making this the first true '
        'generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful '
        'of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated '
        'Lorem Ipsum is therefore always free from repetition, injected humour.'
    ),
    'body': (
        'Among the major reasons why Python is “slow”, it really boils down to 2 — Python is interpreted '
        'as opposed to compiled, ultimately leading to slower execution times; and the fact that it is '
        'dynamically typed. Take, for example, TensorFlow, a Machine Learning library available in Python. '
        'These libraries were actually written in C++ and made available in Python, sort of forming a Python '
        'implementation. The same goes for Numpy and, to an extent, even Caer.'
    ),
    'sidebar_details': [
        {'icon': f'{EDUMIM_IMG}/svg/circle-clock.svg', 'text': '4:00 pm - 6:00 pm'},
        {'icon': f'{EDUMIM_IMG}/svg/circle-c.svg', 'text': '03 March, 2022'},
        {'icon': f'{EDUMIM_IMG}/svg/circle-clock.svg', 'text': '12/A, NewYork Sydney City'},
        {'icon': f'{EDUMIM_IMG}/svg/circle-clock.svg', 'text': 'yourmail@gmail.com'},
        {'icon': f'{EDUMIM_IMG}/svg/circle-clock.svg', 'text': '+88018 2829 98267'},
    ],
    'guests': [
        {'image': f'{EDUMIM_IMG}/all-img/rc-1.png', 'name': 'Sofia d. Flora', 'role': 'UI/UX Designer'},
        {'image': f'{EDUMIM_IMG}/all-img/rc-2.png', 'name': 'Jhonson Steven', 'role': 'UI/UX Designer'},
    ],
}

def _catalog_course_card(image_num):
    return {
        'image': f'{EDUMIM_IMG}/all-img/c{image_num}.png',
        'tag': 'Art & Design',
        'price': '$29.28',
        'title': 'Basic Fundamentals of Interior & Graphics Design',
        'lessons': '2 Lessons',
        'duration': '4h 30m',
        'rating': '4.8',
    }


FILTERED_COURSE_GRID = [_catalog_course_card(n) for n in [1, 2, 3, 4, 5, 6, 7, 1]]
FILTERED_COURSE_LIST = [_catalog_course_card(n) for n in range(1, 8)]

SINGLE_COURSE = {
    'title': 'UI/UX Design and Graphics Learning Bootcamp 2022',
    'tag': 'Data Science',
    'hero_image': f'{EDUMIM_IMG}/all-img/single-course-thumb.png',
    'trainer': 'Md Shamim Hossain',
    'trainer_image': f'{EDUMIM_IMG}/all-img/author-1.png',
    'last_update': '10 February, 2022',
    'instructor_name': 'Daniel Smith',
    'instructor_role': 'User Experience Designer',
    'instructor_image': f'{EDUMIM_IMG}/all-img/ux.png',
}

SINGLE_COURSE_RELATED = [
    {'image': f'{EDUMIM_IMG}/all-img/rc-{n}.png', 'title': 'Greatest Passion In...', 'price': '$38.00'}
    for n in range(1, 4)
]

EDUMIM_PAGES = {
    'home-two': ('Home Two', 'Alternative homepage layout from the original Edumim template.'),
    'home-three': ('Home Three', 'Third homepage variation with the same original visual identity.'),
    'about': ('About 1', 'Institutional about page based on the Edumim pages set.'),
    'about-two': ('About 2', 'Secondary about layout from the original template pages.'),
    'instructor': ('Instructor', 'Team and instructors listing page from Edumim pages.'),
    'instructor-two': ('Instructor 2', 'Second instructors variation from the template.'),
    'instructor-details': ('Instructor Single', 'Detailed profile layout from Edumim pages.'),
    'event': ('Event', 'Events listing page from the original template package.'),
    'event-single': ('Event Single', 'Event details layout from the template.'),
    'courses': ('Courses', 'Courses catalog layout from Edumim pages.'),
    'courses-sidebar': ('Courses Sidebar', 'Courses list with sidebar variant from Edumim.'),
    'single-course': ('Single Course', 'Course detail page from the original Edumim set.'),
    'blog-standard': ('Blog Standard', 'Blog listing standard page as provided in template.'),
    'single-blog': ('Single Blog', 'Blog details page from Edumim package.'),
    'error': ('404', 'Error page layout from the original template.'),
    'contacts': ('Contacts', 'Contact layout matching Edumim pages.'),
}

PRODUCT_PAGE_ALIASES = {
    'solucoes': ('Soluções', 'Visão geral das soluções escolares no layout Edumim.'),
    'solucoes/controle-de-acesso-escolar': ('Controle de acesso escolar', 'Entrada e saída monitoradas para alunos, responsáveis e visitantes.'),
    'solucoes/catraca-eletronica': ('Catraca eletrônica', 'Fluxo com regras por perfil e trilha de auditoria.'),
    'solucoes/cameras-de-monitoramento': ('Câmeras de monitoramento', 'Visão operacional em tempo real para apoio à segurança.'),
    'solucoes/portaria-escolar': ('Portaria escolar', 'Gestão de portaria, visitantes e prestadores.'),
    'solucoes/comunicacao-com-responsaveis': ('Comunicação com responsáveis', 'Comunicados, confirmações e notificações centralizadas.'),
    'solucoes/autorizacoes-e-saidas': ('Autorizações e saídas', 'Fluxo digital de autorização com histórico rastreável.'),
    'solucoes/ocorrencias-escolares': ('Ocorrências escolares', 'Registro e acompanhamento de ocorrências por unidade.'),
    'solucoes/carteirinha-digital': ('Carteirinha digital', 'Identificação digital para acesso e validações internas.'),
    'solucoes/pagamentos-e-cantina-escolar': ('Pagamentos e cantina escolar', 'Gestão de saldo, consumo e pagamentos internos.'),
    'solucoes/cantina-pagamentos': ('Cantina e pagamentos', 'Página equivalente para compatibilidade de rota.'),
    'solucoes/pedido-de-lanche-no-recreio': ('Pedido de lanche no recreio', 'Fluxo aluno-responsável para pedido no intervalo.'),
    'solucoes/visitantes-e-prestadores': ('Visitantes e prestadores', 'Cadastro prévio e controle de acesso de terceiros.'),
    'solucoes/dashboard-para-direcao': ('Dashboard para direção', 'Indicadores de acesso, segurança e operação escolar.'),
    'recursos': ('Recursos', 'Página institucional de recursos no padrão Edumim.'),
    'modulos': ('Módulos', 'Módulos da plataforma apresentados no layout do template.'),
    'planos': ('Preços e Planos', 'Página de preços no padrão visual do template.'),
    'faq': ('FAQ', 'Perguntas frequentes na estrutura Edumim.'),
    'demonstracao': ('Solicitar apresentação', 'Formulário inicial para demonstração comercial.'),
}


def _home_context():
    return {
        'courses': HOME_ONE_COURSES,
        'topics': HOME_ONE_TOPICS,
        'team': HOME_ONE_TEAM,
        'blogs': HOME_ONE_BLOGS,
    }


def _render_page(request, title, subtitle, page_key=''):
    context = {
        'title': title,
        'subtitle': subtitle,
        'page_key': page_key,
    }
    return render(request, 'public_site/edumim/page.html', context)


def home(request):
    return render(request, 'public_site/index.html', _home_context())


def home_two(request):
    context = {
        'categories': HOME_TWO_CATEGORIES,
        'home_two_modules': HOME_TWO_MODULES,
        'home_two_counters': HOME_TWO_COUNTERS,
        'home_two_brands': HOME_TWO_BRANDS,
        'home_two_plans': HOME_TWO_PLANS,
        'home_two_posts': HOME_TWO_POSTS,
        'home_two_instagram': HOME_TWO_INSTAGRAM,
    }
    return render(request, 'public_site/edumim/home_two.html', context)


def home_three(request):
    context = {
        'home_three_brands': HOME_THREE_BRANDS,
        'home_three_courses': HOME_THREE_COURSES,
        'home_three_team': HOME_THREE_TEAM,
        'home_three_events': HOME_THREE_EVENTS,
        'home_three_faq': HOME_THREE_FAQ,
        'home_three_testimonials': HOME_THREE_TESTIMONIALS,
        'home_three_posts': HOME_TWO_POSTS,
    }
    return render(request, 'public_site/edumim/home_three.html', context)


def about(request):
    context = {
        'page_banner_title': 'About Us',
        'page_banner_num': 1,
        'counters': HOME_TWO_COUNTERS,
        'team_rect': HOME_THREE_TEAM,
        'faq_items': HOME_THREE_FAQ,
    }
    return render(request, 'public_site/edumim/about_one.html', context)


def about_two(request):
    context = {
        'page_banner_title': 'About Us',
        'page_banner_num': 2,
        'topics': HOME_ONE_TOPICS,
        'team': HOME_ONE_TEAM,
        'brands': HOME_TWO_BRANDS,
    }
    return render(request, 'public_site/edumim/about_two.html', context)


def instructor(request):
    context = {
        'page_banner_title': 'Instructor',
        'page_banner_num': 1,
        'team': HOME_ONE_TEAM,
        'testimonials': INSTRUCTOR_ONE_TESTIMONIALS,
        'brands': HOME_TWO_BRANDS,
    }
    return render(request, 'public_site/edumim/instructor_one.html', context)


def instructor_two(request):
    context = {
        'page_banner_title': 'Instructor',
        'page_banner_num': 2,
        'team_rect': HOME_THREE_TEAM,
    }
    return render(request, 'public_site/edumim/instructor_two.html', context)


def instructor_details(request):
    context = {
        'page_banner_title': 'About Instructor',
        'page_banner_crumb': 'Team Member 1',
        'instructor': INSTRUCTOR_PROFILE,
        'instructor_stats': INSTRUCTOR_PROFILE_STATS,
        'courses': INSTRUCTOR_PROFILE_COURSES,
    }
    return render(request, 'public_site/edumim/instructor_details.html', context)


def event(request):
    context = {
        'page_banner_title': 'Events',
        'page_banner_crumb': 'Events',
        'events': EVENT_LIST_ITEMS,
    }
    return render(request, 'public_site/edumim/event.html', context)


def event_single(request):
    context = {
        'page_banner_title': EVENT_DETAIL['title'],
        'page_banner_crumb': 'Events',
        'event': EVENT_DETAIL,
    }
    return render(request, 'public_site/edumim/event_single.html', context)


def courses(request):
    context = {
        'page_banner_title': 'Courses',
        'page_banner_crumb': 'Courses',
        'course_grid': FILTERED_COURSE_GRID,
        'course_list': FILTERED_COURSE_LIST,
        'grid_cols': 'lg:grid-cols-3 md:grid-cols-2 grid-cols-1',
        'list_cols': 'lg:grid-cols-2 md:grid-cols-1 grid-cols-1',
    }
    return render(request, 'public_site/edumim/courses.html', context)


def courses_sidebar(request):
    context = {
        'page_banner_title': 'Courses',
        'page_banner_crumb': 'Courses',
        'course_grid': FILTERED_COURSE_GRID,
        'course_list': FILTERED_COURSE_LIST,
        'grid_cols': 'md:grid-cols-2 grid-cols-1',
        'list_cols': 'grid-cols-1',
        'show_filter_sidebar': True,
    }
    return render(request, 'public_site/edumim/courses_sidebar.html', context)


def single_course(request):
    context = {
        'page_banner_title': 'Course Details',
        'page_banner_crumb': 'Course Details',
        'course': SINGLE_COURSE,
        'related_courses': SINGLE_COURSE_RELATED,
    }
    return render(request, 'public_site/edumim/single_course.html', context)


def blog_standard(request):
    context = {
        'page_banner_title': 'Blog Standard',
        'page_banner_crumb': 'Blog Standard',
        'posts': BLOG_STANDARD_POSTS,
        'sidebar_related': BLOG_SIDEBAR_RELATED,
        'instagram_feed': BLOG_INSTAGRAM_FEED,
        'popular_tags': BLOG_POPULAR_TAGS,
    }
    return render(request, 'public_site/edumim/blog.html', context)


def single_blog(request, slug='analytics-customers-properly-1'):
    list_post = next((p for p in BLOG_STANDARD_POSTS if p['slug'] == slug), BLOG_STANDARD_POSTS[0])
    post = {**SINGLE_BLOG_DETAIL, 'slug': list_post['slug']}
    context = {
        'page_banner_title': 'Blog Details',
        'page_banner_crumb': 'Blog Details',
        'post': post,
        'sidebar_related': BLOG_SIDEBAR_RELATED,
        'instagram_feed': BLOG_INSTAGRAM_FEED,
        'popular_tags': BLOG_POPULAR_TAGS,
    }
    return render(request, 'public_site/edumim/blog_detail.html', context)


def blog(request):
    return blog_standard(request)


def contacts(request):
    success = request.GET.get('success', '') == '1'
    if request.method == 'POST':
        full_name = request.POST.get('full-name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        consent = request.POST.get('lgpd_consent') == 'on'

        if full_name and email and consent:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            PrivacyConsentLog.objects.create(
                name=full_name,
                email=email,
                phone=phone,
                source='contato',
                consent_text='Li e aceito a Política de Privacidade e autorizo o contato para atendimento da minha solicitação.',
                ip_address=ip,
                user_agent=user_agent,
            )
            return redirect('/contato/?success=1')

    return render(request, 'public_site/edumim/contact.html', {'success': success, 'title': EDUMIM_PAGES['contacts'][0], 'subtitle': EDUMIM_PAGES['contacts'][1], 'page_key': 'contacts'})


def contact(request):
    return contacts(request)


def error_page(request):
    return _render_page(request, *EDUMIM_PAGES['error'], page_key='error')


def privacy(request):
    return _render_page(request, 'Privacy Policy', 'Legal and privacy content placeholder on Edumim layout.', page_key='privacy')


def terms(request):
    return _render_page(request, 'Terms of Use', 'Terms content placeholder on Edumim layout.', page_key='terms')


def public_login(request):
    return _render_page(request, 'Login', 'Access page in Edumim structure. Use /app/login/ for operational backoffice login.', page_key='login')


def demo(request):
    return _render_page(request, 'Request Demo', 'Schedule a PortalK12/EscolaSegura product presentation.', page_key='demo')


def product_page(request, section='', slug=''):
    key = f'{section}/{slug}'.strip('/')
    if key not in PRODUCT_PAGE_ALIASES:
        return redirect('public_site:home')
    title, subtitle = PRODUCT_PAGE_ALIASES[key]
    return _render_page(request, title, subtitle, page_key=key.replace('/', '-'))


def services(request):
    return redirect('public_site:solutions')


def projects(request):
    return redirect('public_site:resources')
