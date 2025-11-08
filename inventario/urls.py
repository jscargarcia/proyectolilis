from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    # Movimientos de inventario
    path('movimientos/', views.movimiento_listar, name='movimiento_listar'),
    path('movimientos/crear/', views.movimiento_crear, name='movimiento_crear'),
    path('movimientos/<int:pk>/', views.movimiento_detalle, name='movimiento_detalle'),
    path('movimientos/<int:pk>/confirmar/', views.movimiento_confirmar, name='movimiento_confirmar'),
    
    # Stock actual
    path('stock/', views.stock_listar, name='stock_listar'),
    
    # Alertas de stock
    path('alertas/', views.alerta_listar, name='alerta_listar'),
    path('alertas/<int:pk>/resolver/', views.alerta_resolver, name='alerta_resolver'),
]