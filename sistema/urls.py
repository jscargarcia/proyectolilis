from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Carrito - API
    path('carrito/api/', views.carrito_listar, name='carrito_listar'),
    path('carrito/agregar/', views.carrito_agregar, name='carrito_agregar'),
    path('carrito/eliminar/<str:item_id>/', views.carrito_eliminar, name='carrito_eliminar'),
    path('carrito/vaciar/', views.carrito_vaciar, name='carrito_vaciar'),
    path('carrito/count/', views.carrito_count, name='carrito_count'),
    path('carrito/actualizar/<str:item_id>/', views.carrito_actualizar_cantidad, name='carrito_actualizar_cantidad'),
    
    # Carrito - Vista HTML
    path('carrito/', views.carrito_ver, name='carrito_ver'),
    
    # Notificaciones
    path('notificaciones/', views.notificaciones_listar, name='notificaciones_listar'),
    path('notificaciones/agregar/', views.notificaciones_agregar, name='notificaciones_agregar'),
    path('notificaciones/marcar-leida/<int:notif_id>/', views.notificaciones_marcar_leida, name='notificaciones_marcar_leida'),
    path('notificaciones/limpiar/', views.notificaciones_limpiar, name='notificaciones_limpiar'),
    path('notificaciones/count/', views.notificaciones_count, name='notificaciones_count'),
]
