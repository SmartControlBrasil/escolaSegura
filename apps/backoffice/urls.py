from django.urls import path
from . import views

app_name = 'backoffice'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('clientes/', views.clientes, name='clientes'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('orcamentos/', views.orcamentos, name='orcamentos'),
    path('orcamentos/novo/', views.orcamentos_novo, name='orcamentos_novo'),
    path('vistorias/', views.vistorias, name='vistorias'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('redes-sociais/', views.redes_sociais, name='redes_sociais'),
    path('growth/', views.growth, name='growth'),
    path('atlas/', views.atlas, name='atlas'),
    path('assistente/', views.assistente, name='assistente'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
]
