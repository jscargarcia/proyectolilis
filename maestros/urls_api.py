"""
URLs para la API REST del módulo maestros
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    ProductoViewSet, CategoriaViewSet, MarcaViewSet, 
    UnidadMedidaViewSet, ProveedorViewSet
)

# Crear el router automático que genera las URLs REST
router = DefaultRouter()

# Registrar los ViewSets en el router
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'marcas', MarcaViewSet, basename='marca')
router.register(r'unidades-medida', UnidadMedidaViewSet, basename='unidadmedida')
router.register(r'proveedores', ProveedorViewSet, basename='proveedor')

# El router genera automáticamente estas URLs:
# /api/maestros/productos/          -> GET (listar), POST (crear)
# /api/maestros/productos/{id}/     -> GET (ver), PUT (editar), PATCH (editar parcial), DELETE (eliminar)
# /api/maestros/productos/activos/  -> GET (endpoint personalizado)
# /api/maestros/productos/buscar/   -> GET (endpoint personalizado)
# /api/maestros/productos/{id}/cambiar_estado/ -> POST (endpoint personalizado)

urlpatterns = [
    path('', include(router.urls)),
]