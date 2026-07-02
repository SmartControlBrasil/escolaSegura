from django.urls import path

from . import views

app_name = 'parent_portal'

urlpatterns = [
    path('manifest.json', views.manifest_json, name='manifest'),
    path('service-worker.js', views.service_worker_js, name='service_worker'),
    path('', views.dashboard, name='dashboard'),
    path('alunos/<int:student_id>/', views.student_detail, name='student_detail'),
    path('alunos/<int:student_id>/frequencia/', views.attendance, name='attendance'),
    path('alunos/<int:student_id>/comunicados/', views.announcements, name='announcements'),
    path('alunos/<int:student_id>/mensagens/', views.messages, name='messages'),
    path('alunos/<int:student_id>/autorizacoes/', views.authorizations, name='authorizations'),
    path('alunos/<int:student_id>/boletim/', views.report_card, name='report_card'),
]
