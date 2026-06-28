from django.urls import path
from . import views

app_name = 'backoffice'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('clientes/', views.clientes, name='clientes'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('orcamentos/', views.orcamentos, name='orcamentos'),
    path('vistorias/', views.vistorias, name='vistorias'),
    path('relatorios/', views.relatorios, name='relatorios'),
]
