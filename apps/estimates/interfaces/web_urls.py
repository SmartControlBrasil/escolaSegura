from django.urls import path
from apps.estimates.interfaces.views import estimate_builder, estimates_dashboard, mobile_inspection

urlpatterns = [
    path('', estimates_dashboard, name='estimates-dashboard'),
    path('builder/', estimate_builder, name='estimates-builder'),
    path('builder/<uuid:estimate_id>/', estimate_builder, name='estimates-builder-edit'),
    path('<uuid:estimate_id>/vistoria/', mobile_inspection, name='estimates-mobile-inspection'),
]
