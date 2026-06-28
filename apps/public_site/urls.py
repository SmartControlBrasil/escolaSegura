from django.urls import path
from . import views

app_name = 'public_site'

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre/', views.about, name='about'),
    path('servicos/', views.services, name='services'),
    path('projetos/', views.projects, name='projects'),
    path('blog/', views.blog, name='blog'),
    path('contato/', views.contact, name='contact'),
    path('privacidade/', views.privacy, name='privacy'),
    path('termos/', views.terms, name='terms'),
]
