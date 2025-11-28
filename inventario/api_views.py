"""
API Views para el módulo inventario - Django REST Framework
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum, Count
from django.utils import timezone
from datetime import timedelta

from .models import MovimientoInventario, StockActual, AlertaStock, Bodega, Lote
from .serializers import (
    MovimientoInventarioSerializer, MovimientoInventarioListSerializer,
    StockActualSerializer, StockActualListSerializer,
    AlertaStockSerializer, BodegaSerializer, LoteSerializer
)


class BodegaViewSet(viewsets.ModelViewSet):
    """ViewSet para el modelo Bodega"""
    queryset = Bodega.objects.all()
    serializer_class = BodegaSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'activo']
    search_fields = ['codigo', 'nombre', 'direccion']
    ordering_fields = ['nombre', 'created_at']
    ordering = ['nombre']
    
    def get_queryset(self):
        """Filtrar bodegas activas por defecto"""
        queryset = super().get_queryset()
        
        solo_activos = self.request.query_params.get('solo_activos', 'true')
        if solo_activos.lower() == 'true':
            queryset = queryset.filter(activo=True)
            
        return queryset
    
    @action(detail=True, methods=['get'])
    def stock(self, request, pk=None):
        """Obtener stock de una bodega"""
        bodega = self.get_object()
        stocks = StockActual.objects.filter(bodega=bodega, cantidad_disponible__gt=0)
        serializer = StockActualListSerializer(stocks, many=True)
        return Response(serializer.data)


class MovimientoInventarioViewSet(viewsets.ModelViewSet):
    """ViewSet para MovimientoInventario"""
    queryset = MovimientoInventario.objects.select_related(
        'producto', 'bodega_origen', 'bodega_destino', 'proveedor', 'usuario'
    ).all()
    serializer_class = MovimientoInventarioSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo_movimiento', 'estado', 'bodega_origen', 'bodega_destino', 'producto']
    search_fields = ['producto__nombre', 'producto__sku', 'observaciones']
    ordering_fields = ['fecha_movimiento', 'cantidad', 'precio_unitario']
    ordering = ['-fecha_movimiento']
    
    def get_serializer_class(self):
        """Usar serializer simplificado para listas"""
        if self.action == 'list':
            return MovimientoInventarioListSerializer
        return MovimientoInventarioSerializer
    
    def perform_create(self, serializer):
        """Asignar usuario al crear movimiento"""
        serializer.save(usuario=self.request.user)
    
    @action(detail=False, methods=['get'])
    def ingresos(self, request):
        """Endpoint: /api/inventario/movimientos/ingresos/"""
        movimientos = self.get_queryset().filter(tipo_movimiento='INGRESO')
        
        # Filtros adicionales
        fecha_desde = request.query_params.get('fecha_desde')
        fecha_hasta = request.query_params.get('fecha_hasta')
        
        if fecha_desde:
            movimientos = movimientos.filter(fecha_movimiento__gte=fecha_desde)
        if fecha_hasta:
            movimientos = movimientos.filter(fecha_movimiento__lte=fecha_hasta)
        
        page = self.paginate_queryset(movimientos)
        if page is not None:
            serializer = MovimientoInventarioListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = MovimientoInventarioListSerializer(movimientos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def salidas(self, request):
        """Endpoint: /api/inventario/movimientos/salidas/"""
        movimientos = self.get_queryset().filter(tipo_movimiento='SALIDA')
        
        fecha_desde = request.query_params.get('fecha_desde')
        fecha_hasta = request.query_params.get('fecha_hasta')
        
        if fecha_desde:
            movimientos = movimientos.filter(fecha_movimiento__gte=fecha_desde)
        if fecha_hasta:
            movimientos = movimientos.filter(fecha_movimiento__lte=fecha_hasta)
        
        page = self.paginate_queryset(movimientos)
        if page is not None:
            serializer = MovimientoInventarioListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = MovimientoInventarioListSerializer(movimientos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """Endpoint: /api/inventario/movimientos/estadisticas/"""
        # Últimos 30 días
        fecha_limite = timezone.now() - timedelta(days=30)
        
        movimientos = self.get_queryset().filter(
            fecha_movimiento__gte=fecha_limite,
            estado='CONFIRMADO'
        )
        
        stats = {
            'total_movimientos': movimientos.count(),
            'total_ingresos': movimientos.filter(tipo_movimiento='INGRESO').count(),
            'total_salidas': movimientos.filter(tipo_movimiento='SALIDA').count(),
            'valor_total_ingresos': movimientos.filter(
                tipo_movimiento='INGRESO'
            ).aggregate(
                total=Sum('cantidad') * Sum('precio_unitario')
            )['total'] or 0,
            'productos_mas_movidos': movimientos.values(
                'producto__nombre'
            ).annotate(
                total_movimientos=Count('id')
            ).order_by('-total_movimientos')[:5]
        }
        
        return Response(stats)


class StockActualViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para StockActual
    Solo permite GET (listar y ver)
    """
    queryset = StockActual.objects.select_related(
        'producto', 'bodega'
    ).all()
    serializer_class = StockActualSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['producto', 'bodega']
    search_fields = ['producto__nombre', 'producto__sku', 'bodega__nombre']
    ordering_fields = ['cantidad_disponible', 'producto__nombre']
    ordering = ['producto__nombre']
    
    def get_serializer_class(self):
        """Usar serializer simplificado para listas"""
        if self.action == 'list':
            return StockActualListSerializer
        return StockActualSerializer
    
    def get_queryset(self):
        """Filtrar stock con cantidad mayor a 0 por defecto"""
        queryset = super().get_queryset()
        
        con_stock = self.request.query_params.get('con_stock', 'true')
        if con_stock.lower() == 'true':
            queryset = queryset.filter(cantidad_disponible__gt=0)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def bajo_minimo(self, request):
        """Stock por debajo del mínimo"""
        from django.db.models import F
        
        stock_bajo = self.get_queryset().filter(
            cantidad_disponible__lte=F('producto__stock_minimo')
        )
        
        serializer = StockActualListSerializer(stock_bajo, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def sin_stock(self, request):
        """Productos sin stock"""
        sin_stock = self.get_queryset().filter(cantidad_disponible=0)
        serializer = StockActualListSerializer(sin_stock, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def resumen(self, request):
        """Resumen general del stock"""
        queryset = self.get_queryset()
        
        resumen = {
            'total_productos_con_stock': queryset.filter(cantidad_disponible__gt=0).count(),
            'total_productos_sin_stock': queryset.filter(cantidad_disponible=0).count(),
            'productos_bajo_minimo': queryset.filter(
                cantidad_disponible__lte=F('producto__stock_minimo')
            ).count(),
            'valor_total_inventario': 0,  # Requiere cálculo más complejo
        }
        
        return Response(resumen)


class AlertaStockViewSet(viewsets.ModelViewSet):
    """ViewSet para AlertaStock"""
    queryset = AlertaStock.objects.select_related(
        'producto', 'bodega', 'resuelto_por'
    ).all()
    serializer_class = AlertaStockSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo_alerta', 'prioridad', 'estado', 'producto', 'bodega']
    search_fields = ['producto__nombre', 'mensaje']
    ordering_fields = ['fecha_generacion', 'prioridad']
    ordering = ['-fecha_generacion']
    
    @action(detail=True, methods=['post'])
    def resolver(self, request, pk=None):
        """Resolver una alerta"""
        alerta = self.get_object()
        observaciones = request.data.get('observaciones', '')
        
        alerta.estado = 'RESUELTA'
        alerta.fecha_resolucion = timezone.now()
        alerta.resuelto_por = request.user
        alerta.observaciones_resolucion = observaciones
        alerta.save()
        
        serializer = self.get_serializer(alerta)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def activas(self, request):
        """Alertas activas"""
        alertas_activas = self.get_queryset().filter(estado='ACTIVA')
        serializer = self.get_serializer(alertas_activas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def criticas(self, request):
        """Alertas críticas"""
        alertas_criticas = self.get_queryset().filter(
            estado='ACTIVA', 
            prioridad='CRITICA'
        )
        serializer = self.get_serializer(alertas_criticas, many=True)
        return Response(serializer.data)


class LoteViewSet(viewsets.ModelViewSet):
    """ViewSet para Lote"""
    queryset = Lote.objects.select_related('producto').all()
    serializer_class = LoteSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['producto', 'activo']
    search_fields = ['numero_lote', 'producto__nombre']
    ordering_fields = ['fecha_vencimiento', 'created_at']
    ordering = ['fecha_vencimiento']
    
    @action(detail=False, methods=['get'])
    def por_vencer(self, request):
        """Lotes próximos a vencer (30 días)"""
        fecha_limite = timezone.now().date() + timedelta(days=30)
        lotes_por_vencer = self.get_queryset().filter(
            fecha_vencimiento__lte=fecha_limite,
            activo=True
        )
        serializer = self.get_serializer(lotes_por_vencer, many=True)
        return Response(serializer.data)