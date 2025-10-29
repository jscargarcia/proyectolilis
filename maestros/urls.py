from django.urls import path
from . import views

urlpatterns = [
    # Productos
    path('productos/', views.producto_listar, name='producto_listar'),
    path('productos/crear/', views.producto_crear, name='producto_crear'),
    path('productos/<int:pk>/', views.producto_detalle, name='producto_detalle'),
    path('productos/<int:pk>/editar/', views.producto_editar, name='producto_editar'),
    path('productos/<int:pk>/eliminar/', views.producto_eliminar, name='producto_eliminar'),
    path('productos/<int:pk>/test-eliminar/', views.test_producto_eliminar, name='test_producto_eliminar'),
    
    # Proveedores
    path('proveedores/', views.proveedor_listar, name='proveedor_listar'),
    path('proveedores/crear/', views.proveedor_crear, name='proveedor_crear'),
    path('proveedores/<int:pk>/', views.proveedor_detalle, name='proveedor_detalle'),
    
    # Categorías
    path('categorias/', views.categoria_listar, name='categoria_listar'),
    
    # Marcas
    path('marcas/', views.marca_listar, name='marca_listar'),
]
