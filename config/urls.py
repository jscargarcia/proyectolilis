"""
URL configuration for LilyBE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('autenticacion:dashboard')
    else:
        return redirect('autenticacion:login')

def demo_alertas(request):
    """Vista para demostrar el sistema de alertas"""
    return render(request, 'demo_alertas.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_redirect, name='home'),
    path('auth/', include('autenticacion.urls')),
    path('catalogo/', include('catalogo.urls')),
    path('api/', include('sistema.urls')),
    path('ventas/', include('ventas.urls')),
    path('maestros/', include('maestros.urls')),
    path('productos/', include('productos.urls')),
    path('inventario/', include('inventario.urls')),
    path('demo/alertas/', demo_alertas, name='demo_alertas'),
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    if hasattr(settings, 'MEDIA_URL') and hasattr(settings, 'MEDIA_ROOT'):
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

