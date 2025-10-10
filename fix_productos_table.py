"""
Script para agregar las columnas faltantes a la tabla productos
"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def main():
    print("="*80)
    print("AGREGANDO COLUMNAS FALTANTES A LA TABLA 'productos'")
    print("="*80)
    print()

    with connection.cursor() as cursor:
        print("Verificando columnas existentes...")
        cursor.execute("SHOW COLUMNS FROM productos")
        columnas_existentes = [col[0] for col in cursor.fetchall()]
        print(f"Columnas actuales: {len(columnas_existentes)}")
        print()
        
        # Paso 1: Agregar columnas como NULL primero
        print("PASO 1: Agregando columnas como NULL...")
        print("-" * 80)
        
        columnas_paso1 = [
            ('categoria_id', 'ALTER TABLE productos ADD COLUMN categoria_id bigint NULL AFTER descripcion'),
            ('marca_id', 'ALTER TABLE productos ADD COLUMN marca_id bigint NULL AFTER categoria_id'),
            ('uom_compra_id', 'ALTER TABLE productos ADD COLUMN uom_compra_id bigint NULL AFTER modelo'),
            ('uom_venta_id', 'ALTER TABLE productos ADD COLUMN uom_venta_id bigint NULL AFTER uom_compra_id'),
            ('uom_stock_id', 'ALTER TABLE productos ADD COLUMN uom_stock_id bigint NULL AFTER uom_venta_id'),
            ('dias_vida_util', 'ALTER TABLE productos ADD COLUMN dias_vida_util int NULL AFTER perishable'),
        ]
        
        for nombre, sql in columnas_paso1:
            if nombre not in columnas_existentes:
                try:
                    cursor.execute(sql)
                    print(f"  ✓ Columna '{nombre}' agregada como NULL")
                except Exception as e:
                    if 'Duplicate column' not in str(e):
                        print(f"  ✗ Error: {e}")
            else:
                print(f"  ✓ Columna '{nombre}' ya existe")
        
        print()
        
        # Paso 2: Obtener IDs por defecto
        print("PASO 2: Obteniendo IDs por defecto...")
        print("-" * 80)
        
        # Obtener primera categoría
        cursor.execute("SELECT id FROM categorias LIMIT 1")
        categoria_default = cursor.fetchone()
        if categoria_default:
            categoria_id = categoria_default[0]
            print(f"  ✓ Categoría por defecto: ID {categoria_id}")
        else:
            # Crear una categoría por defecto
            cursor.execute("INSERT INTO categorias (nombre, descripcion, activo, created_at) VALUES ('General', 'Categoría por defecto', 1, NOW())")
            categoria_id = cursor.lastrowid
            print(f"  ✓ Categoría 'General' creada: ID {categoria_id}")
        
        # Obtener primera unidad de medida
        cursor.execute("SELECT id FROM unidades_medida WHERE codigo = 'UND' LIMIT 1")
        uom_default = cursor.fetchone()
        if uom_default:
            uom_id = uom_default[0]
            print(f"  ✓ Unidad de medida por defecto (UND): ID {uom_id}")
        else:
            cursor.execute("SELECT id FROM unidades_medida LIMIT 1")
            uom_default = cursor.fetchone()
            if uom_default:
                uom_id = uom_default[0]
                print(f"  ✓ Unidad de medida por defecto: ID {uom_id}")
            else:
                print("  ⚠ No hay unidades de medida, ejecuta seed_simple.py primero")
                print("\nAbortando proceso. Por favor ejecuta:")
                print("  python seed_simple.py")
                sys.exit(1)
        
        print()
        
        # Paso 3: Actualizar valores NULL con valores por defecto
        print("PASO 3: Actualizando valores NULL...")
        print("-" * 80)
        
        cursor.execute("UPDATE productos SET categoria_id = %s WHERE categoria_id IS NULL", [categoria_id])
        print(f"  ✓ Categorías actualizadas: {cursor.rowcount} registros")
        
        cursor.execute("UPDATE productos SET uom_compra_id = %s WHERE uom_compra_id IS NULL", [uom_id])
        print(f"  ✓ UOM Compra actualizadas: {cursor.rowcount} registros")
        
        cursor.execute("UPDATE productos SET uom_venta_id = %s WHERE uom_venta_id IS NULL", [uom_id])
        print(f"  ✓ UOM Venta actualizadas: {cursor.rowcount} registros")
        
        cursor.execute("UPDATE productos SET uom_stock_id = %s WHERE uom_stock_id IS NULL", [uom_id])
        print(f"  ✓ UOM Stock actualizadas: {cursor.rowcount} registros")
        
        print()
        
        # Paso 4: Agregar restricciones NOT NULL
        print("PASO 4: Agregando restricciones NOT NULL...")
        print("-" * 80)
        
        restricciones = [
            ('categoria_id NOT NULL', 'ALTER TABLE productos MODIFY categoria_id bigint NOT NULL'),
            ('uom_compra_id NOT NULL', 'ALTER TABLE productos MODIFY uom_compra_id bigint NOT NULL'),
            ('uom_venta_id NOT NULL', 'ALTER TABLE productos MODIFY uom_venta_id bigint NOT NULL'),
            ('uom_stock_id NOT NULL', 'ALTER TABLE productos MODIFY uom_stock_id bigint NOT NULL'),
        ]
        
        for desc, sql in restricciones:
            try:
                cursor.execute(sql)
                print(f"  ✓ {desc}")
            except Exception as e:
                print(f"  ✗ Error en {desc}: {e}")
        
        print()
        
        # Paso 5: Agregar índices y FKs
        print("PASO 5: Agregando índices y Foreign Keys...")
        print("-" * 80)
        
        indices_fks = [
            ('idx_productos_categoria', 'CREATE INDEX idx_productos_categoria ON productos(categoria_id)'),
            ('fk_productos_categoria', 'ALTER TABLE productos ADD CONSTRAINT fk_productos_categoria FOREIGN KEY (categoria_id) REFERENCES categorias(id)'),
            ('idx_productos_marca', 'CREATE INDEX idx_productos_marca ON productos(marca_id)'),
            ('fk_productos_marca', 'ALTER TABLE productos ADD CONSTRAINT fk_productos_marca FOREIGN KEY (marca_id) REFERENCES marcas(id)'),
            ('idx_productos_uom_compra', 'CREATE INDEX idx_productos_uom_compra ON productos(uom_compra_id)'),
            ('fk_productos_uom_compra', 'ALTER TABLE productos ADD CONSTRAINT fk_productos_uom_compra FOREIGN KEY (uom_compra_id) REFERENCES unidades_medida(id)'),
            ('idx_productos_uom_venta', 'CREATE INDEX idx_productos_uom_venta ON productos(uom_venta_id)'),
            ('fk_productos_uom_venta', 'ALTER TABLE productos ADD CONSTRAINT fk_productos_uom_venta FOREIGN KEY (uom_venta_id) REFERENCES unidades_medida(id)'),
            ('idx_productos_uom_stock', 'CREATE INDEX idx_productos_uom_stock ON productos(uom_stock_id)'),
            ('fk_productos_uom_stock', 'ALTER TABLE productos ADD CONSTRAINT fk_productos_uom_stock FOREIGN KEY (uom_stock_id) REFERENCES unidades_medida(id)'),
        ]
        
        for nombre, sql in indices_fks:
            try:
                cursor.execute(sql)
                print(f"  ✓ {nombre} creado")
            except Exception as e:
                if 'Duplicate' in str(e) or 'already exists' in str(e):
                    print(f"  ✓ {nombre} ya existe")
                else:
                    print(f"  ⚠ {nombre}: {e}")
        
        print()
        
        # Verificar el resultado final
        print("="*80)
        print("VERIFICACIÓN FINAL")
        print("="*80)
        
        cursor.execute("SHOW COLUMNS FROM productos")
        columnas_finales = cursor.fetchall()
        
        print(f"\nTotal de columnas en la tabla: {len(columnas_finales)}")
        print("\nColumnas de ForeignKey agregadas:")
        for col in columnas_finales:
            if col[0].endswith('_id') and col[0] not in ['id']:
                print(f"  ✓ {col[0]} ({col[1]})")
        
        print("\n✅ ¡Proceso completado exitosamente!")
        print("\nAhora puedes acceder a /admin/maestros/producto/ sin errores.")
        print()

if __name__ == '__main__':
    main()
