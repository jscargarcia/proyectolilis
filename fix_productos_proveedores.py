"""
Script para agregar la columna producto_id a la tabla productos_proveedores
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def main():
    print("="*80)
    print("AGREGANDO COLUMNA producto_id A productos_proveedores")
    print("="*80)
    print()

    with connection.cursor() as cursor:
        # Verificar columnas existentes
        cursor.execute("SHOW COLUMNS FROM productos_proveedores")
        columnas_existentes = [col[0] for col in cursor.fetchall()]
        
        print(f"Columnas actuales: {', '.join(columnas_existentes)}")
        print()
        
        if 'producto_id' in columnas_existentes:
            print("✓ La columna 'producto_id' ya existe")
            return
        
        # Paso 1: Agregar columna como NULL
        print("PASO 1: Agregando columna producto_id como NULL...")
        print("-" * 80)
        try:
            cursor.execute("""
                ALTER TABLE productos_proveedores 
                ADD COLUMN producto_id bigint NULL AFTER id
            """)
            print("  ✓ Columna 'producto_id' agregada como NULL")
        except Exception as e:
            print(f"  ✗ Error: {e}")
            return
        
        print()
        
        # Paso 2: Verificar si hay datos
        cursor.execute("SELECT COUNT(*) FROM productos_proveedores")
        count = cursor.fetchone()[0]
        print(f"PASO 2: Verificando datos existentes...")
        print("-" * 80)
        print(f"  Registros en la tabla: {count}")
        
        if count > 0:
            # Si hay datos, necesitamos asignar un producto por defecto
            cursor.execute("SELECT id FROM productos LIMIT 1")
            producto_default = cursor.fetchone()
            
            if producto_default:
                producto_id = producto_default[0]
                print(f"  ✓ Producto por defecto: ID {producto_id}")
                
                cursor.execute(
                    "UPDATE productos_proveedores SET producto_id = %s WHERE producto_id IS NULL",
                    [producto_id]
                )
                print(f"  ✓ Actualizados {cursor.rowcount} registros")
            else:
                print("  ⚠ No hay productos en la tabla 'productos'")
                print("  ⚠ Se mantendrá como NULL")
        else:
            print("  ✓ No hay datos, continuando...")
        
        print()
        
        # Paso 3: Agregar restricción NOT NULL
        print("PASO 3: Agregando restricción NOT NULL...")
        print("-" * 80)
        try:
            cursor.execute("""
                ALTER TABLE productos_proveedores 
                MODIFY producto_id bigint NOT NULL
            """)
            print("  ✓ Restricción NOT NULL agregada")
        except Exception as e:
            print(f"  ✗ Error: {e}")
        
        print()
        
        # Paso 4: Agregar índice
        print("PASO 4: Agregando índice...")
        print("-" * 80)
        try:
            cursor.execute("""
                CREATE INDEX idx_productos_proveedores_producto 
                ON productos_proveedores(producto_id)
            """)
            print("  ✓ Índice creado")
        except Exception as e:
            if 'Duplicate' in str(e):
                print("  ✓ Índice ya existe")
            else:
                print(f"  ⚠ Error: {e}")
        
        print()
        
        # Paso 5: Agregar Foreign Key
        print("PASO 5: Agregando Foreign Key...")
        print("-" * 80)
        try:
            cursor.execute("""
                ALTER TABLE productos_proveedores 
                ADD CONSTRAINT fk_productos_proveedores_producto 
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            """)
            print("  ✓ Foreign Key creada")
        except Exception as e:
            if 'already exists' in str(e):
                print("  ✓ Foreign Key ya existe")
            else:
                print(f"  ⚠ Error: {e}")
        
        print()
        
        # Verificación final
        print("="*80)
        print("VERIFICACIÓN FINAL")
        print("="*80)
        
        cursor.execute("SHOW COLUMNS FROM productos_proveedores")
        columnas_finales = cursor.fetchall()
        
        print(f"\nTotal de columnas: {len(columnas_finales)}")
        print("\nColumnas de ForeignKey:")
        for col in columnas_finales:
            if col[0].endswith('_id'):
                print(f"  ✓ {col[0]} ({col[1]})")
        
        print("\n✅ ¡Proceso completado exitosamente!")
        print("\nAhora puedes agregar productos desde el admin sin errores.")
        print()

if __name__ == '__main__':
    main()
