"""
URLs para el módulo inventario (vistas web)
"""
from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    # Dashboard
    path('', views.dashboard_inventario, name='dashboard'),
    
    # Movimientos de inventario
    path('movimientos/', views.movimiento_listar, name='movimiento_listar'),
    path('movimientos/crear/', views.movimiento_crear, name='movimiento_crear'),
    path('movimientos/<int:pk>/', views.movimiento_detalle, name='movimiento_detalle'),
    path('movimientos/<int:pk>/confirmar/', views.movimiento_confirmar, name='movimiento_confirmar'),
    
    # Ingresos y Salidas específicos
    path('ingresos/registrar/', views.registrar_ingreso, name='registrar_ingreso'),
    path('salidas/registrar/', views.registrar_salida, name='registrar_salida'),
    
    # Stock actual
    path('stock/', views.vista_stock_actual, name='stock_listar'),
    path('stock/actual/', views.vista_stock_actual, name='vista_stock_actual'),  # Alias por compatibilidad
    
    # Historial
    path('historial/', views.historial_movimientos, name='historial_movimientos'),
    
    # Alertas de stock
    path('alertas/', views.alerta_listar, name='alerta_listar'),
    path('alertas/<int:pk>/resolver/', views.alerta_resolver, name='alerta_resolver'),
    path('alertas/regenerar/', views.alerta_regenerar, name='alerta_regenerar'),
    
    # API endpoints básicos
    path('api/stock-producto/', views.obtener_stock_producto, name='obtener_stock_producto'),
    path('api/productos/search/', views.productos_search_api, name='productos_search_api'),
    path('api/bodegas/', views.bodegas_api, name='bodegas_api'),
    path('api/proveedores/', views.proveedores_api, name='proveedores_api'),
]