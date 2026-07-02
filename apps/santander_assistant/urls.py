from django.urls import path

from apps.santander_assistant import views

app_name = 'santander_assistant'

urlpatterns = [
    path('chat/', views.chat_endpoint, name='chat'),
    path('greeting/', views.greeting_endpoint, name='greeting'),
]
