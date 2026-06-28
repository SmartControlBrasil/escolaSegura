from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.catalog.interfaces.views import ProductCategoryViewSet, ProductImageViewSet, ProductItemViewSet, ProductViewSet

router = DefaultRouter()
router.register('categories', ProductCategoryViewSet)
router.register('products', ProductViewSet)
router.register('product-items', ProductItemViewSet)
router.register('product-images', ProductImageViewSet)
urlpatterns = [path('', include(router.urls))]
