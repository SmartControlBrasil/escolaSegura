from rest_framework import serializers
from apps.service_reports.infrastructure.models import ServiceReport, ServiceReportItem, ServiceReportPhoto


class ServiceReportItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceReportItem
        fields = ['id','report','description','quantity','unit','unit_price','subtotal','is_billable','notes','created_at','updated_at']
        read_only_fields = ['id','report','subtotal','created_at','updated_at']


class ServiceReportPhotoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ServiceReportPhoto
        fields = ['id','report','image','image_url','category','caption','technical_notes','taken_at','uploaded_by','created_at','updated_at']
        read_only_fields = ['id','image_url','uploaded_by','created_at','updated_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None


class ServiceReportSerializer(serializers.ModelSerializer):
    items = ServiceReportItemSerializer(many=True, read_only=True)
    photos = ServiceReportPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceReport
        fields = [
            'id','organization','customer','estimate','sales_order','number','title','status','service_date','service_location',
            'technician_name','problem_reported','service_performed','recommendations','customer_signature_name',
            'started_at','finished_at','total_amount','created_by','items','photos','created_at','updated_at'
        ]
        read_only_fields = ['id','number','total_amount','created_by','created_at','updated_at']
