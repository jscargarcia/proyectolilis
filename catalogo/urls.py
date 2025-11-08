from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.catalogo_listar, name='catalogo_listar'),
    path('crear/', views.catalogo_crear, name='catalogo_crear'),
    path('<int:pk>/', views.catalogo_detalle, name='catalogo_detalle'),
    path('<int:pk>/editar/', views.catalogo_editar, name='catalogo_editar'),
    path('<int:pk>/eliminar/', views.catalogo_eliminar, name='catalogo_eliminar'),
    path('<int:pk>/publicar/', views.catalogo_publicar, name='catalogo_publicar'),
]
