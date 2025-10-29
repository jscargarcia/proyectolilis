from django.urls import path
from . import views

urlpatterns = [
    # Clientes
    path('clientes/', views.cliente_listar, name='cliente_listar'),
    path('clientes/crear/', views.cliente_crear, name='cliente_crear'),
    path('clientes/<int:pk>/', views.cliente_detalle, name='cliente_detalle'),
    path('clientes/<int:pk>/editar/', views.cliente_editar, name='cliente_editar'),
    path('clientes/<int:pk>/eliminar/', views.cliente_eliminar, name='cliente_eliminar'),
    
    # Ventas
    path('', views.venta_listar, name='venta_listar'),
    path('crear/', views.venta_crear, name='venta_crear'),
    path('<int:pk>/', views.venta_detalle, name='venta_detalle'),
    path('<int:pk>/editar/', views.venta_editar, name='venta_editar'),
    path('<int:pk>/eliminar/', views.venta_eliminar, name='venta_eliminar'),
    path('<int:pk>/cambiar-estado/', views.venta_cambiar_estado, name='venta_cambiar_estado'),
]
