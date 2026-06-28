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
    
    # Vistorias
    path('vistorias/', views.vistorias, name='vistorias'),
    path('vistorias/novo/', views.vistorias_novo, name='vistorias_novo'),
    path('vistorias/<uuid:id>/', views.vistorias_detalhe, name='vistorias_detalhe'),
    
    # Outros
    path('relatorios/', views.relatorios, name='relatorios'),
    path('redes-sociais/', views.redes_sociais, name='redes_sociais'),
    path('growth/', views.growth, name='growth'),
    path('atlas/', views.atlas, name='atlas'),
    path('assistente/', views.assistente, name='assistente'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
]
