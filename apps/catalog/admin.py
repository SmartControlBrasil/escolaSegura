from django.contrib import admin
from apps.catalog.infrastructure.models import Product, ProductCategory, ProductImage, ProductItem

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fk_name = 'product'
    extra = 0
    fields = ['image','kind','title','caption','sort_order','is_public']


class ProductItemInline(admin.TabularInline):
    model = ProductItem
    fk_name = 'product'
    extra = 0

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug','organization','is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name','slug']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','sku','type','category','sale_price','is_active']
    list_filter = ['type','category','is_active']
    search_fields = ['name','sku','description']
    inlines = [ProductImageInline, ProductItemInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product','kind','title','sort_order','is_public','created_at']
    list_filter = ['kind','is_public']
    search_fields = ['product__name','title','caption','alt_text']
