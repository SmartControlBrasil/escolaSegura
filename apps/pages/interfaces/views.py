from rest_framework import viewsets
from apps.pages.infrastructure.models import HtmlPage
from apps.pages.interfaces.serializers import HtmlPageSerializer

class HtmlPageViewSet(viewsets.ModelViewSet):
    queryset = HtmlPage.objects.all()
    serializer_class = HtmlPageSerializer
    search_fields = ['title','slug','seo_title','seo_description']
    filterset_fields = ['organization','status']
