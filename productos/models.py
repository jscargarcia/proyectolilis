# Los modelos de productos están definidos en la app 'maestros'
# Esta app solo contiene las vistas y templates para el módulo de productos

# Importar modelos desde maestros para mantener compatibilidad
from maestros.models import Producto, Categoria, Marca, UnidadMedida, Proveedor, ProductoProveedor
