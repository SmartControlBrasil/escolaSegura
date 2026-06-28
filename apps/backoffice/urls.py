from django.urls import path
from . import views

app_name = 'backoffice'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Clientes
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/novo/', views.clientes_novo, name='clientes_novo'),
    path('clientes/<uuid:id>/', views.clientes_detalhe, name='clientes_detalhe'),
    
    # Catálogo
    path('catalogo/', views.catalogo, name='catalogo'),
    path('catalogo/novo/', views.catalogo_novo, name='catalogo_novo'),
    path('catalogo/<uuid:id>/', views.catalogo_detalhe, name='catalogo_detalhe'),
    
    # Orçamentos
    path('orcamentos/', views.orcamentos, name='orcamentos'),
    path('orcamentos/novo/', views.orcamentos_novo, name='orcamentos_novo'),
    path('orcamentos/<uuid:id>/', views.orcamentos_detalhe, name='orcamentos_detalhe'),
    path('orcamentos/<uuid:id>/preview/', views.orcamentos_preview, name='orcamentos_preview'),
    path('orcamentos/<uuid:id>/pdf/', views.orcamentos_pdf, name='orcamentos_pdf'),
    
    # Vistorias
    path('vistorias/', views.vistorias, name='vistorias'),
    path('vistorias/novo/', views.vistorias_novo, name='vistorias_novo'),
    path('vistorias/<uuid:id>/', views.vistorias_detalhe, name='vistorias_detalhe'),
    
    # Entregas de Obra
    path('entregas/', views.entregas, name='entregas'),
    path('entregas/nova/', views.entregas_novo, name='entregas_novo'),
    path('entregas/<uuid:id>/', views.entregas_detalhe, name='entregas_detalhe'),
    path('entregas/<uuid:id>/preview/', views.entregas_preview, name='entregas_preview'),
    path('entregas/<uuid:id>/pdf/', views.entregas_pdf, name='entregas_pdf'),

    # Obras / Projetos
    path('obras/', views.obras, name='obras'),
    path('obras/nova/', views.obras_novo, name='obras_novo'),
    path('obras/<uuid:id>/', views.obras_detalhe, name='obras_detalhe'),

    # Veículos
    path('veiculos/', views.veiculos, name='veiculos'),
    path('veiculos/novo/', views.veiculos_novo, name='veiculos_novo'),
    path('veiculos/<uuid:id>/', views.veiculos_detalhe, name='veiculos_detalhe'),

    # Fornecedores
    path('fornecedores/', views.fornecedores, name='fornecedores'),
    path('fornecedores/novo/', views.fornecedores_novo, name='fornecedores_novo'),
    path('fornecedores/<uuid:id>/', views.fornecedores_detalhe, name='fornecedores_detalhe'),

    # Financeiro
    path('financeiro/', views.financeiro, name='financeiro'),
    path('financeiro/novo/', views.financeiro_novo, name='financeiro_novo'),
    path('financeiro/<uuid:id>/', views.financeiro_detalhe, name='financeiro_detalhe'),

    # Usuários
    path('usuarios/', views.usuarios, name='usuarios'),
    path('usuarios/novo/', views.usuarios_novo, name='usuarios_novo'),
    path('usuarios/<uuid:id>/', views.usuarios_detalhe, name='usuarios_detalhe'),

    # Outros
    path('relatorios/', views.relatorios, name='relatorios'),
    path('redes-sociais/', views.redes_sociais, name='redes_sociais'),
    path('growth/', views.growth, name='growth'),
    path('atlas/', views.atlas, name='atlas'),
    path('assistente/', views.assistente, name='assistente'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
]
