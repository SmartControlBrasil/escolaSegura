from django.urls import path
from . import views

app_name = 'public_site'

urlpatterns = [
    # Edumim home set
    path('', views.home, name='home'),
    path('home-two/', views.home_two, name='home_two'),
    path('home-three/', views.home_three, name='home_three'),

    # Edumim pages menu
    path('about/', views.about, name='about'),
    path('about-two/', views.about_two, name='about_two'),
    path('instructor/', views.instructor, name='instructor'),
    path('instructor-two/', views.instructor_two, name='instructor_two'),
    path('instructor-details/', views.instructor_details, name='instructor_details'),
    path('event/', views.event, name='event'),
    path('event-single/', views.event_single, name='event_single'),
    path('courses/', views.courses, name='courses'),
    path('courses-sidebar/', views.courses_sidebar, name='courses_sidebar'),
    path('single-course/', views.single_course, name='single_course'),
    path('blog-standard/', views.blog_standard, name='blog_standard'),
    path('single-blog/', views.single_blog, name='single_blog'),
    path('single-blog/<slug:slug>/', views.single_blog, name='single_blog_slug'),
    path('contacts/', views.contacts, name='contacts'),
    path('error/', views.error_page, name='error'),

    # Product/institutional aliases requested
    path('sobre/', views.about, name='about_pt'),
    path('solucoes/', views.product_page, {'section': 'solucoes', 'slug': ''}, name='solutions'),
    path('solucoes/<slug:slug>/', views.product_page, {'section': 'solucoes'}, name='solution_detail'),
    path('recursos/', views.product_page, {'section': 'recursos', 'slug': ''}, name='resources'),
    path('modulos/', views.product_page, {'section': 'modulos', 'slug': ''}, name='modules'),
    path('planos/', views.product_page, {'section': 'planos', 'slug': ''}, name='pricing'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.single_blog, name='blog_detail'),
    path('faq/', views.product_page, {'section': 'faq', 'slug': ''}, name='faq'),
    path('contato/', views.contact, name='contact'),
    path('login/', views.public_login, name='public_login'),
    path('demonstracao/', views.demo, name='demo'),
    path('privacidade/', views.privacy, name='privacy'),
    path('termos/', views.terms, name='terms'),

    # Legacy aliases
    path('servicos/', views.services, name='services'),
    path('projetos/', views.projects, name='projects'),
]
