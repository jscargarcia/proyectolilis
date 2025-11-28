"""
Serializers para el módulo maestros - Django REST Framework
Convierte modelos de Django a formato JSON y viceversa
"""
from rest_framework import serializers
from .models import Producto, Categoria, Marca, UnidadMedida, Proveedor


class CategoriaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Categoria"""
    
    class Meta:
        model = Categoria
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class MarcaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Marca"""
    
    class Meta:
        model = Marca
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class UnidadMedidaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo UnidadMedida"""
    
    class Meta:
        model = UnidadMedida
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class ProductoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Producto
    Incluye relaciones anidadas para mejor información
    """
    # Campos de solo lectura con información detallada
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    marca_nombre = serializers.CharField(source='marca.nombre', read_only=True)
    uom_compra_nombre = serializers.CharField(source='uom_compra.nombre', read_only=True)
    uom_venta_nombre = serializers.CharField(source='uom_venta.nombre', read_only=True)
    uom_stock_nombre = serializers.CharField(source='uom_stock.nombre', read_only=True)
    
    # Serializers anidados para relaciones (opcional)
    categoria_detalle = CategoriaSerializer(source='categoria', read_only=True)
    marca_detalle = MarcaSerializer(source='marca', read_only=True)
    uom_compra_detalle = UnidadMedidaSerializer(source='uom_compra', read_only=True)
    uom_venta_detalle = UnidadMedidaSerializer(source='uom_venta', read_only=True)
    uom_stock_detalle = UnidadMedidaSerializer(source='uom_stock', read_only=True)
    
    class Meta:
        model = Producto
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def validate_sku(self, value):
        """Validar que el SKU sea único y tenga formato válido"""
        if self.instance and self.instance.sku == value:
            return value
            
        if Producto.objects.filter(sku=value).exists():
            raise serializers.ValidationError("Ya existe un producto con este SKU.")
        
        if len(value) < 3:
            raise serializers.ValidationError("El SKU debe tener al menos 3 caracteres.")
            
        return value.upper()
    
    def validate_precio_venta(self, value):
        """Validar que el precio de venta sea positivo"""
        if value is not None and value <= 0:
            raise serializers.ValidationError("El precio de venta debe ser mayor a 0.")
        return value
    
    def validate_stock_minimo(self, value):
        """Validar que el stock mínimo sea positivo"""
        if value is not None and value < 0:
            raise serializers.ValidationError("El stock mínimo no puede ser negativo.")
        return value


class ProveedorSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Proveedor"""
    
    class Meta:
        model = Proveedor
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def validate_rut_nif(self, value):
        """Validar formato del RUT/NIF"""
        if self.instance and self.instance.rut_nif == value:
            return value
            
        if Proveedor.objects.filter(rut_nif=value).exists():
            raise serializers.ValidationError("Ya existe un proveedor con este RUT/NIF.")
        
        if len(value) < 8:
            raise serializers.ValidationError("El RUT/NIF debe tener al menos 8 caracteres.")
            
        return value.upper()
    
    def validate_email(self, value):
        """Validar formato del email"""
        if not value:
            return value
            
        # Validación adicional si es necesaria
        if '@' not in value:
            raise serializers.ValidationError("Formato de email inválido.")
            
        return value.lower()


# Serializer simplificado para listas
class ProductoListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listar productos"""
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    marca_nombre = serializers.CharField(source='marca.nombre', read_only=True)
    
    class Meta:
        model = Producto
        fields = ['id', 'sku', 'nombre', 'categoria_nombre', 'marca_nombre', 
                 'precio_venta', 'stock_minimo', 'estado']


class ProveedorListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listar proveedores"""
    
    class Meta:
        model = Proveedor
        fields = ['id', 'rut_nif', 'razon_social', 'nombre_fantasia', 
                 'email', 'telefono', 'estado']