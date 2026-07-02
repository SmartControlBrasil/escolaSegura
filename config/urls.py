from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from apps.core.api.views import HealthCheckAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/health/', HealthCheckAPIView.as_view(), name='api-health'),
    path('api/v1/auth/token/', obtain_auth_token, name='api-token'),
    path('api/v1/core/', include('apps.core.interfaces.urls')),
    path('api/v1/accounts/', include('apps.accounts.interfaces.urls')),
    path('api/v1/customers/', include('apps.customers.interfaces.urls')),
    path('api/v1/catalog/', include('apps.catalog.interfaces.urls')),
    path('api/v1/inventory/', include('apps.inventory.interfaces.urls')),
    path('api/v1/sales/', include('apps.sales.interfaces.urls')),
    path('api/v1/estimates/', include('apps.estimates.interfaces.urls')),
    path('api/v1/service-reports/', include('apps.service_reports.interfaces.urls')),
    path('api/v1/finance/', include('apps.finance.interfaces.urls')),
    path('api/v1/agents/', include('apps.agents.interfaces.urls')),
    path('api/v1/policy/', include('apps.policy_guard.interfaces.urls')),
    path('api/v1/integrations/', include('apps.integrations.interfaces.urls')),
    path('api/v1/pages/', include('apps.pages.interfaces.urls')),
    path('app/estimates/', include('apps.estimates.interfaces.web_urls')),
    path('app/service-reports/', include('apps.service_reports.interfaces.web_urls')),
    path('assistant/', include('apps.escola_segura_assistant.urls')),
    path('', include('apps.public_site.urls')),
    path('app/', include('apps.backoffice.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
