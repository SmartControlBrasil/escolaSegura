from django.urls import path

from apps.escola_segura_assistant import views

app_name = 'escola_segura_assistant'

urlpatterns = [
    path('chat/', views.chat_endpoint, name='chat'),
    path('greeting/', views.greeting_endpoint, name='greeting'),
]
