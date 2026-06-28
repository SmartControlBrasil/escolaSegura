from decimal import Decimal
from django.db import models
from apps.core.infrastructure.models import TimeStampedModel

class ProductCategory(TimeStampedModel):
    organization = models.ForeignKey('core.Organization', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        unique_together = [('organization','slug')]

    def __str__(self):
        return self.name

class Product(TimeStampedModel):
    class Type(models.TextChoices):
        PRODUCT = 'product', 'Produto'
        SERVICE = 'service', 'Serviço'
        PART = 'part', 'Peça'
        ACCESSORY = 'accessory', 'Acessório'

    organization = models.ForeignKey('core.Organization', null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(ProductCategory, null=True, blank=True, on_delete=models.SET_NULL, related_name='products')
    name = models.CharField(max_length=180)
    sku = models.CharField(max_length=80, blank=True, db_index=True)
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.PRODUCT)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=20, default='un')
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    is_active = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['name']
        unique_together = [('organization','sku')]

    def __str__(self):
        return self.name

class ProductItem(TimeStampedModel):
    class ItemKind(models.TextChoices):
        COMPONENT = 'component', 'Componente'
        KIT_ITEM = 'kit_item', 'Item de Kit'
        ACCESSORY = 'accessory', 'Acessório'
        SPARE_PART = 'spare_part', 'Peça de reposição'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    linked_product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL, related_name='used_in_items')
    kind = models.CharField(max_length=30, choices=ItemKind.choices, default=ItemKind.COMPONENT)
    name = models.CharField(max_length=180)
    sku = models.CharField(max_length=80, blank=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=3, default=Decimal('1.000'))
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['product__name','name']

    def __str__(self):
        return f'{self.product} -> {self.name}'


class ProductImage(TimeStampedModel):
    class ImageKind(models.TextChoices):
        PRIMARY = 'primary', 'Principal'
        GALLERY = 'gallery', 'Galeria'
        TECHNICAL = 'technical', 'Técnica'
        BEFORE_AFTER = 'before_after', 'Antes/depois'
        DOCUMENT = 'document', 'Documento'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='catalog/products/%Y/%m/')
    kind = models.CharField(max_length=30, choices=ImageKind.choices, default=ImageKind.GALLERY)
    title = models.CharField(max_length=160, blank=True)
    caption = models.TextField(blank=True)
    alt_text = models.CharField(max_length=180, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_public = models.BooleanField(default=True)

    class Meta:
        ordering = ['product__name', 'sort_order', 'created_at']

    def __str__(self):
        return self.title or f'Imagem de {self.product}'
