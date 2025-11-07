from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/cambiar-password/', views.cambiar_password, name='cambiar_password'),
    path('solicitar-codigo-cambio/', views.solicitar_codigo_cambio, name='solicitar_codigo_cambio'),
    path('verificar-codigo-cambio/', views.verificar_codigo_cambio, name='verificar_codigo_cambio'),
    path('recuperar-password/', views.recuperar_password, name='recuperar_password'),
    path('verificar-codigo-recuperacion/', views.verificar_codigo_recuperacion, name='verificar_codigo_recuperacion'),
    path('resetear-password/<str:token>/', views.resetear_password, name='resetear_password'),
    path('api/eliminar-avatar/', views.eliminar_avatar, name='eliminar_avatar'),
]
