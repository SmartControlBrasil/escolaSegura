from rest_framework import serializers
from apps.catalog.infrastructure.models import Product, ProductCategory, ProductImage, ProductItem

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id','organization','name','slug','description','is_active','created_at','updated_at']
        read_only_fields = ['id','created_at','updated_at']

class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductItem
        fields = ['id','product','linked_product','kind','name','sku','quantity','notes','created_at','updated_at']
        read_only_fields = ['id','created_at','updated_at']

class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id','product','image','image_url','kind','title','caption','alt_text','sort_order','is_public','created_at','updated_at']
        read_only_fields = ['id','image_url','created_at','updated_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None


class ProductSerializer(serializers.ModelSerializer):
    items = ProductItemSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id','organization','category','name','sku','type','description','unit','sale_price','cost_price','is_active','metadata','items','images','created_at','updated_at']
        read_only_fields = ['id','created_at','updated_at']
