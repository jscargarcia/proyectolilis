from django.urls import path
from . import views

app_name = 'autenticacion'

urlpatterns = [
    # Autenticación
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Perfil de usuario
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/cambiar-password/', views.cambiar_password, name='cambiar_password'),
    path('solicitar-codigo-cambio/', views.solicitar_codigo_cambio, name='solicitar_codigo_cambio'),
    path('verificar-codigo-cambio/', views.verificar_codigo_cambio, name='verificar_codigo_cambio'),
    path('recuperar-password/', views.recuperar_password, name='recuperar_password'),
    path('verificar-codigo-recuperacion/', views.verificar_codigo_recuperacion, name='verificar_codigo_recuperacion'),
    path('resetear-password/<str:token>/', views.resetear_password, name='resetear_password'),
    path('api/eliminar-avatar/', views.eliminar_avatar, name='eliminar_avatar'),
    
    # Gestión de usuarios (CRUD)
    path('usuarios/', views.usuario_listar, name='usuario_listar'),
    path('usuarios/crear/', views.usuario_crear, name='usuario_crear'),
    path('usuarios/<int:pk>/', views.usuario_detalle, name='usuario_detalle'),
    path('usuarios/<int:pk>/editar/', views.usuario_editar, name='usuario_editar'),
    path('usuarios/<int:pk>/cambiar-estado/', views.usuario_cambiar_estado, name='usuario_cambiar_estado'),
    path('usuarios/<int:pk>/resetear-password/', views.usuario_resetear_password, name='usuario_resetear_password'),
    path('usuarios/<int:pk>/historial/', views.usuario_historial, name='usuario_historial'),
    path('usuarios/<int:pk>/eliminar/', views.usuario_eliminar, name='usuario_eliminar'),
    
    # Gestión de roles
    path('roles/', views.rol_listar, name='rol_listar'),
    path('roles/crear/', views.rol_crear, name='rol_crear'),
    path('roles/<int:pk>/editar/', views.rol_editar, name='rol_editar'),
]
