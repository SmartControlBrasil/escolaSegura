from rest_framework import serializers
from apps.pages.infrastructure.models import HtmlPage

class HtmlPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HtmlPage
        fields = '__all__'
