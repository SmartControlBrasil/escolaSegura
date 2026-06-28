from rest_framework import viewsets
from apps.catalog.infrastructure.models import Product, ProductCategory, ProductImage, ProductItem
from apps.catalog.interfaces.serializers import ProductCategorySerializer, ProductImageSerializer, ProductItemSerializer, ProductSerializer

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    search_fields = ['name','slug','description']
    filterset_fields = ['organization','is_active']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').prefetch_related('items').all()
    serializer_class = ProductSerializer
    search_fields = ['name','sku','description']
    filterset_fields = ['organization','category','type','is_active']
    ordering_fields = ['name','sale_price','created_at']

class ProductItemViewSet(viewsets.ModelViewSet):
    queryset = ProductItem.objects.select_related('product','linked_product').all()
    serializer_class = ProductItemSerializer
    search_fields = ['name','sku','notes']
    filterset_fields = ['product','linked_product','kind']


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.select_related('product').all()
    serializer_class = ProductImageSerializer
    search_fields = ['title','caption','alt_text','product__name','product__sku']
    filterset_fields = ['product','kind','is_public']
    ordering_fields = ['sort_order','created_at']
