"""
Serializers para el módulo inventario - Django REST Framework
"""
from rest_framework import serializers
from .models import MovimientoInventario, StockActual, AlertaStock, Bodega, Lote
from maestros.serializers import ProductoListSerializer, ProveedorListSerializer


class BodegaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Bodega"""
    
    class Meta:
        model = Bodega
        fields = '__all__'
        read_only_fields = ('created_at',)


class LoteSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Lote"""
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    
    class Meta:
        model = Lote
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class StockActualSerializer(serializers.ModelSerializer):
    """Serializer para el modelo StockActual"""
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    producto_sku = serializers.CharField(source='producto.sku', read_only=True)
    bodega_nombre = serializers.CharField(source='bodega.nombre', read_only=True)
    
    # Stock total calculado
    stock_total = serializers.SerializerMethodField()
    
    class Meta:
        model = StockActual
        fields = '__all__'
        read_only_fields = ('updated_at',)
    
    def get_stock_total(self, obj):
        """Calcular stock total (disponible + reservado + tránsito)"""
        return obj.cantidad_disponible + obj.cantidad_reservada + obj.cantidad_transito


class MovimientoInventarioSerializer(serializers.ModelSerializer):
    """Serializer para el modelo MovimientoInventario"""
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    producto_sku = serializers.CharField(source='producto.sku', read_only=True)
    bodega_origen_nombre = serializers.CharField(source='bodega_origen.nombre', read_only=True)
    bodega_destino_nombre = serializers.CharField(source='bodega_destino.nombre', read_only=True)
    proveedor_nombre = serializers.CharField(source='proveedor.razon_social', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.get_full_name', read_only=True)
    
    # Valor total del movimiento
    valor_total = serializers.SerializerMethodField()
    
    class Meta:
        model = MovimientoInventario
        fields = '__all__'
        read_only_fields = ('fecha_movimiento', 'usuario')
    
    def get_valor_total(self, obj):
        """Calcular valor total del movimiento"""
        if obj.cantidad and obj.precio_unitario:
            return float(obj.cantidad) * float(obj.precio_unitario)
        return 0
    
    def validate(self, data):
        """Validaciones personalizadas"""
        tipo_movimiento = data.get('tipo_movimiento')
        bodega_origen = data.get('bodega_origen')
        bodega_destino = data.get('bodega_destino')
        
        # Validar que salidas tengan bodega origen
        if tipo_movimiento == 'SALIDA' and not bodega_origen:
            raise serializers.ValidationError(
                "Los movimientos de salida requieren bodega origen"
            )
        
        # Validar que ingresos tengan bodega destino
        if tipo_movimiento == 'INGRESO' and not bodega_destino:
            raise serializers.ValidationError(
                "Los movimientos de ingreso requieren bodega destino"
            )
        
        # Validar que transferencias tengan ambas bodegas
        if tipo_movimiento == 'TRANSFERENCIA':
            if not bodega_origen or not bodega_destino:
                raise serializers.ValidationError(
                    "Las transferencias requieren bodega origen y destino"
                )
            if bodega_origen == bodega_destino:
                raise serializers.ValidationError(
                    "Las bodegas origen y destino deben ser diferentes"
                )
        
        return data
    
    def validate_cantidad(self, value):
        """Validar que la cantidad sea positiva"""
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a 0")
        return value


class AlertaStockSerializer(serializers.ModelSerializer):
    """Serializer para el modelo AlertaStock"""
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    producto_sku = serializers.CharField(source='producto.sku', read_only=True)
    bodega_nombre = serializers.CharField(source='bodega.nombre', read_only=True)
    resuelto_por_nombre = serializers.CharField(source='resuelto_por.get_full_name', read_only=True)
    
    class Meta:
        model = AlertaStock
        fields = '__all__'
        read_only_fields = ('fecha_generacion', 'fecha_resolucion', 'resuelto_por')


# Serializers simplificados para listas
class MovimientoInventarioListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listar movimientos"""
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    bodega_origen_nombre = serializers.CharField(source='bodega_origen.nombre', read_only=True)
    bodega_destino_nombre = serializers.CharField(source='bodega_destino.nombre', read_only=True)
    valor_total = serializers.SerializerMethodField()
    
    class Meta:
        model = MovimientoInventario
        fields = ['id', 'tipo_movimiento', 'producto_nombre', 'cantidad', 
                 'bodega_origen_nombre', 'bodega_destino_nombre', 'valor_total',
                 'fecha_movimiento', 'estado']
    
    def get_valor_total(self, obj):
        if obj.cantidad and obj.precio_unitario:
            return float(obj.cantidad) * float(obj.precio_unitario)
        return 0


class StockActualListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listar stock"""
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    producto_sku = serializers.CharField(source='producto.sku', read_only=True)
    bodega_nombre = serializers.CharField(source='bodega.nombre', read_only=True)
    
    class Meta:
        model = StockActual
        fields = ['id', 'producto_sku', 'producto_nombre', 'bodega_nombre',
                 'cantidad_disponible', 'cantidad_reservada', 'cantidad_transito']