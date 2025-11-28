"""
URLs para la API REST del módulo inventario
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    MovimientoInventarioViewSet, StockActualViewSet, 
    AlertaStockViewSet, BodegaViewSet, LoteViewSet
)

# Router para endpoints automáticos
router = DefaultRouter()

# Registrar ViewSets
router.register(r'movimientos', MovimientoInventarioViewSet, basename='movimiento')
router.register(r'stock', StockActualViewSet, basename='stock')
router.register(r'alertas', AlertaStockViewSet, basename='alerta')
router.register(r'bodegas', BodegaViewSet, basename='bodega')
router.register(r'lotes', LoteViewSet, basename='lote')

# URLs generadas automáticamente:
# /api/inventario/movimientos/              -> GET, POST
# /api/inventario/movimientos/{id}/         -> GET, PUT, PATCH, DELETE
# /api/inventario/movimientos/ingresos/     -> GET (personalizado)
# /api/inventario/movimientos/salidas/      -> GET (personalizado)
# /api/inventario/movimientos/estadisticas/ -> GET (personalizado)
#
# /api/inventario/stock/                    -> GET (solo lectura)
# /api/inventario/stock/{id}/               -> GET (solo lectura)
# /api/inventario/stock/bajo_minimo/        -> GET (personalizado)
# /api/inventario/stock/sin_stock/          -> GET (personalizado)
# /api/inventario/stock/resumen/            -> GET (personalizado)
#
# /api/inventario/alertas/                  -> GET, POST
# /api/inventario/alertas/{id}/             -> GET, PUT, PATCH, DELETE
# /api/inventario/alertas/{id}/resolver/    -> POST (personalizado)
# /api/inventario/alertas/activas/          -> GET (personalizado)
# /api/inventario/alertas/criticas/         -> GET (personalizado)
#
# /api/inventario/bodegas/                  -> GET, POST
# /api/inventario/bodegas/{id}/             -> GET, PUT, PATCH, DELETE
# /api/inventario/bodegas/{id}/stock/       -> GET (personalizado)
#
# /api/inventario/lotes/                    -> GET, POST
# /api/inventario/lotes/{id}/               -> GET, PUT, PATCH, DELETE
# /api/inventario/lotes/por_vencer/         -> GET (personalizado)

urlpatterns = [
    path('', include(router.urls)),
]