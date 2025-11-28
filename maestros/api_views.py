"""
API Views para el módulo maestros - Django REST Framework
ViewSets que proporcionan operaciones CRUD automáticas
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Producto, Categoria, Marca, UnidadMedida, Proveedor
from .serializers import (
    ProductoSerializer, ProductoListSerializer, 
    CategoriaSerializer, MarcaSerializer, UnidadMedidaSerializer,
    ProveedorSerializer, ProveedorListSerializer
)


class ProductoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Producto
    Proporciona operaciones CRUD automáticas:
    - GET /api/productos/ (listar)
    - GET /api/productos/{id}/ (ver uno)
    - POST /api/productos/ (crear)
    - PUT /api/productos/{id}/ (editar completo)
    - PATCH /api/productos/{id}/ (editar parcial)
    - DELETE /api/productos/{id}/ (eliminar)
    """
    queryset = Producto.objects.select_related(
        'categoria', 'marca', 'uom_compra', 'uom_venta', 'uom_stock'
    ).all()
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]
    
    # Filtros y búsquedas
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categoria', 'marca', 'estado']
    search_fields = ['sku', 'nombre', 'descripcion']
    ordering_fields = ['nombre', 'sku', 'precio_venta', 'created_at']
    ordering = ['nombre']
    
    def get_serializer_class(self):
        """Usar serializer simplificado para listas"""
        if self.action == 'list':
            return ProductoListSerializer
        return ProductoSerializer
    
    def get_queryset(self):
        """Filtrar queryset según parámetros"""
        queryset = super().get_queryset()
        
        # Filtro por estado activo por defecto
        solo_activos = self.request.query_params.get('solo_activos', 'true')
        if solo_activos.lower() == 'true':
            queryset = queryset.filter(estado='ACTIVO')
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def activos(self, request):
        """Endpoint personalizado: /api/productos/activos/"""
        productos_activos = self.get_queryset().filter(estado='ACTIVO')
        serializer = ProductoListSerializer(productos_activos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cambiar_estado(self, request, pk=None):
        """Endpoint personalizado: /api/productos/{id}/cambiar_estado/"""
        producto = self.get_object()
        nuevo_estado = request.data.get('estado')
        
        if nuevo_estado not in ['ACTIVO', 'INACTIVO', 'DESCONTINUADO']:
            return Response(
                {'error': 'Estado inválido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        producto.estado = nuevo_estado
        producto.save()
        
        serializer = self.get_serializer(producto)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def buscar(self, request):
        """Endpoint personalizado: /api/productos/buscar/?q=texto"""
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Parámetro q requerido'}, status=400)
        
        productos = self.get_queryset().filter(
            Q(sku__icontains=query) | 
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query)
        )
        
        serializer = ProductoListSerializer(productos, many=True)
        return Response(serializer.data)


class CategoriaViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo Categoria"""
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'created_at']
    ordering = ['nombre']
    
    @action(detail=True, methods=['get'])
    def productos(self, request, pk=None):
        """Obtener productos de una categoría"""
        categoria = self.get_object()
        productos = categoria.productos.filter(estado='ACTIVO')
        serializer = ProductoListSerializer(productos, many=True)
        return Response(serializer.data)


class MarcaViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo Marca"""
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'created_at']
    ordering = ['nombre']
    
    @action(detail=True, methods=['get'])
    def productos(self, request, pk=None):
        """Obtener productos de una marca"""
        marca = self.get_object()
        productos = marca.productos.filter(estado='ACTIVO')
        serializer = ProductoListSerializer(productos, many=True)
        return Response(serializer.data)


class UnidadMedidaViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo UnidadMedida"""
    queryset = UnidadMedida.objects.all()
    serializer_class = UnidadMedidaSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo']
    search_fields = ['nombre', 'abreviatura']
    ordering_fields = ['nombre', 'created_at']
    ordering = ['nombre']


class ProveedorViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo Proveedor"""
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estado', 'condiciones_pago', 'pais']
    search_fields = ['rut_nif', 'razon_social', 'nombre_fantasia', 'email']
    ordering_fields = ['razon_social', 'created_at']
    ordering = ['razon_social']
    
    def get_serializer_class(self):
        """Usar serializer simplificado para listas"""
        if self.action == 'list':
            return ProveedorListSerializer
        return ProveedorSerializer
    
    def get_queryset(self):
        """Filtrar proveedores activos por defecto"""
        queryset = super().get_queryset()
        
        solo_activos = self.request.query_params.get('solo_activos', 'true')
        if solo_activos.lower() == 'true':
            queryset = queryset.filter(estado='ACTIVO')
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def activos(self, request):
        """Endpoint personalizado: /api/proveedores/activos/"""
        proveedores_activos = self.get_queryset().filter(estado='ACTIVO')
        serializer = ProveedorListSerializer(proveedores_activos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cambiar_estado(self, request, pk=None):
        """Cambiar estado del proveedor"""
        proveedor = self.get_object()
        nuevo_estado = request.data.get('estado')
        
        if nuevo_estado not in ['ACTIVO', 'BLOQUEADO']:
            return Response(
                {'error': 'Estado inválido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        proveedor.estado = nuevo_estado
        proveedor.save()
        
        serializer = self.get_serializer(proveedor)
        return Response(serializer.data)