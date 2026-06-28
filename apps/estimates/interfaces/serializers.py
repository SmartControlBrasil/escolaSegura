from rest_framework import serializers
from apps.estimates.application.services import EstimateService
from apps.estimates.infrastructure.models import Estimate, EstimateContactMessage, EstimateLine, EstimateMeasurement, EstimatePhoto


class EstimateLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstimateLine
        fields = ['id','estimate','product','kind','description','unit','quantity','unit_price','discount_amount','subtotal','sort_order','notes','created_at','updated_at']
        read_only_fields = ['id','estimate','subtotal','created_at','updated_at']


class EstimatePhotoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = EstimatePhoto
        fields = ['id','estimate','image','image_url','category','caption','measurement_notes','taken_at','uploaded_by','latitude','longitude','created_at','updated_at']
        read_only_fields = ['id','image_url','uploaded_by','created_at','updated_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None


class EstimateMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstimateMeasurement
        fields = ['id','estimate','label','value','unit','notes','sort_order','created_at','updated_at']
        read_only_fields = ['id','created_at','updated_at']


class EstimateContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstimateContactMessage
        fields = ['id','estimate','channel','subject','body','status','approved_by_human','sent_at','created_at','updated_at']
        read_only_fields = ['id','sent_at','created_at','updated_at']


class EstimateSerializer(serializers.ModelSerializer):
    lines = EstimateLineSerializer(many=True, read_only=True)
    photos = EstimatePhotoSerializer(many=True, read_only=True)
    measurements = EstimateMeasurementSerializer(many=True, read_only=True)
    input_lines = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Estimate
        fields = [
            'id','organization','customer','sales_order','number','title','status','service_location','visit_scheduled_at',
            'scope_summary','internal_notes','customer_message','terms_and_conditions','validity_days',
            'labor_amount','discount_amount','tax_amount','subtotal_amount','total_amount','created_by','assigned_to',
            'lines','photos','measurements','input_lines','created_at','updated_at'
        ]
        read_only_fields = ['id','number','subtotal_amount','total_amount','created_by','created_at','updated_at']

    def create(self, validated_data):
        lines = validated_data.pop('input_lines', [])
        request = self.context.get('request')
        user = request.user if request and getattr(request.user, 'is_authenticated', False) else None
        return EstimateService.create_estimate(created_by=user, lines=lines, **validated_data)
