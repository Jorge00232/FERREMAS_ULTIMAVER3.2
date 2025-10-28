# api_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import MarcaViewSet, CategoriaViewSet, SubcategoriaViewSet, ProductoViewSet, CarritoItemViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'marcas', MarcaViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'subcategorias', SubcategoriaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'carritoitems', CarritoItemViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
