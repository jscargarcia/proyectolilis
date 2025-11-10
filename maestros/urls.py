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
    path('productos/<int:pk>/desactivar/', views.producto_desactivar, name='producto_desactivar'),
    path('productos/<int:pk>/eliminar/', views.producto_eliminar, name='producto_eliminar'),
    path('productos/<int:pk>/test-eliminar/', views.test_producto_eliminar, name='test_producto_eliminar'),
    path('productos/<int:pk>/test-estado/', views.producto_test_estado, name='producto_test_estado'),
    
    # Proveedores
    path('proveedores/', views.proveedor_listar, name='proveedor_listar'),
    path('proveedores/crear/', views.proveedor_crear, name='proveedor_crear'),
    path('proveedores/exportar-excel/', views.export_proveedores_excel, name='export_proveedores_excel'),
    path('proveedores/<int:pk>/', views.proveedor_detalle, name='proveedor_detalle'),
    path('proveedores/<int:pk>/editar/', views.proveedor_editar, name='proveedor_editar'),
    path('proveedores/<int:pk>/eliminar/', views.proveedor_eliminar, name='proveedor_eliminar'),
    
    # Categorías
    path('categorias/', views.categoria_listar, name='categoria_listar'),
    path('categorias/crear/', views.categoria_crear, name='categoria_crear'),
    path('categorias/exportar-excel/', views.export_categorias_excel, name='export_categorias_excel'),
    path('categorias/<int:pk>/', views.categoria_detalle, name='categoria_detalle'),
    path('categorias/<int:pk>/editar/', views.categoria_editar, name='categoria_editar'),
    path('categorias/<int:pk>/eliminar/', views.categoria_eliminar, name='categoria_eliminar'),
    
    # Marcas
    path('marcas/', views.marca_listar, name='marca_listar'),
    path('marcas/crear/', views.marca_crear, name='marca_crear'),
    path('marcas/exportar-excel/', views.export_marcas_excel, name='export_marcas_excel'),
    path('marcas/<int:pk>/', views.marca_detalle, name='marca_detalle'),
    path('marcas/<int:pk>/editar/', views.marca_editar, name='marca_editar'),
    path('marcas/<int:pk>/eliminar/', views.marca_eliminar, name='marca_eliminar'),
]
