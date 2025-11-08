from django.urls import path
from . import views

app_name = 'maestros'

urlpatterns = [
    # Productos
    path('productos/', views.producto_listar, name='producto_listar'),
    path('productos/crear/', views.producto_crear, name='producto_crear'),
    path('productos/exportar-excel/', views.productos_exportar_excel, name='productos_exportar_excel'),
    path('productos/<int:pk>/', views.producto_detalle, name='producto_detalle'),
    path('productos/<int:pk>/editar/', views.producto_editar, name='producto_editar'),
    path('productos/<int:pk>/eliminar/', views.producto_eliminar, name='producto_eliminar'),
    path('productos/<int:pk>/test-eliminar/', views.test_producto_eliminar, name='test_producto_eliminar'),
    path('productos/<int:pk>/test-estado/', views.producto_test_estado, name='producto_test_estado'),
    
    # Proveedores
    path('proveedores/', views.proveedor_listar, name='proveedor_listar'),
    path('proveedores/crear/', views.proveedor_crear, name='proveedor_crear'),
    path('proveedores/<int:pk>/', views.proveedor_detalle, name='proveedor_detalle'),
    path('proveedores/<int:pk>/editar/', views.proveedor_editar, name='proveedor_editar'),
    path('proveedores/<int:pk>/eliminar/', views.proveedor_eliminar, name='proveedor_eliminar'),
    
    # Categorías
    path('categorias/', views.categoria_listar, name='categoria_listar'),
    
    # Marcas
    path('marcas/', views.marca_listar, name='marca_listar'),
]
