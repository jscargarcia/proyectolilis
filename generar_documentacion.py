"""
Genera un paquete completo de documentación para instalación
"""
import os
from datetime import datetime

def main():
    print()
    print("="*80)
    print(" 📦 GENERANDO DOCUMENTACIÓN DE INSTALACIÓN")
    print("="*80)
    print()
    
    archivos_documentacion = [
        ("README.md", "Descripción general del proyecto"),
        ("INSTRUCTIVO_INSTALACION.md", "Guía paso a paso de instalación"),
        ("CHECKLIST_INSTALACION.md", "Lista de verificación de instalación"),
        ("SISTEMA_VENTAS.md", "Documentación del módulo de ventas"),
        ("SOLUCION_MAESTROS.md", "Soluciones a problemas comunes"),
        ("SEED_README.md", "Información sobre datos de prueba"),
        ("RESUMEN_EJECUTIVO.md", "Resumen ejecutivo del sistema"),
        ("requirements.txt", "Dependencias de Python"),
        ("instalar.ps1", "Script de instalación para Windows"),
        ("instalar.sh", "Script de instalación para Linux/Mac"),
        (".gitignore", "Archivos a ignorar en Git"),
    ]
    
    scripts_utilidad = [
        ("verify_setup.py", "Verificar configuración general"),
        ("verificar_vendedor.py", "Verificar permisos de vendedor"),
        ("resumen_ventas.py", "Ver resumen del sistema"),
        ("check_db.py", "Verificar base de datos"),
        ("check_django_tables.py", "Verificar tablas de Django"),
        ("check_productos_table.py", "Verificar tabla de productos"),
        ("check_productos_proveedores.py", "Verificar tabla productos-proveedores"),
        ("convert_to_innodb.py", "Convertir tablas a InnoDB"),
        ("fix_permissions_tables.py", "Crear tablas de permisos"),
        ("add_permission_fks.py", "Agregar foreign keys de permisos"),
        ("fix_productos_table.py", "Corregir tabla de productos"),
        ("fix_productos_proveedores.py", "Corregir tabla productos-proveedores"),
        ("seed_simple.py", "Cargar datos de ejemplo"),
        ("configurar_permisos_vendedor.py", "Configurar permisos de vendedor"),
        ("crear_clientes_ejemplo.py", "Crear clientes de ejemplo"),
    ]
    
    print("📄 DOCUMENTACIÓN DISPONIBLE:")
    print("-" * 80)
    for archivo, descripcion in archivos_documentacion:
        existe = "✓" if os.path.exists(archivo) else "✗"
        print(f"  {existe} {archivo:<35} - {descripcion}")
    
    print()
    print("🔧 SCRIPTS DE UTILIDAD:")
    print("-" * 80)
    for archivo, descripcion in scripts_utilidad:
        existe = "✓" if os.path.exists(archivo) else "✗"
        print(f"  {existe} {archivo:<40} - {descripcion}")
    
    print()
    print("="*80)
    print(" 📋 RESUMEN PARA NUEVA INSTALACIÓN")
    print("="*80)
    print()
    
    print("1️⃣  LEER PRIMERO:")
    print("    📖 README.md - Visión general del proyecto")
    print()
    
    print("2️⃣  INSTALACIÓN:")
    print("    Windows:")
    print("      .\\instalar.ps1")
    print()
    print("    Linux/Mac:")
    print("      chmod +x instalar.sh")
    print("      ./instalar.sh")
    print()
    print("    O seguir paso a paso:")
    print("      📖 INSTRUCTIVO_INSTALACION.md")
    print()
    
    print("3️⃣  VERIFICACIÓN:")
    print("    ✓ CHECKLIST_INSTALACION.md - Lista completa de verificación")
    print("    ✓ python verify_setup.py - Verificación automática")
    print()
    
    print("4️⃣  DOCUMENTACIÓN ESPECÍFICA:")
    print("    📖 SISTEMA_VENTAS.md - Sistema de ventas")
    print("    📖 SOLUCION_MAESTROS.md - Solución de problemas")
    print()
    
    print("="*80)
    print(" 🎯 ARCHIVOS NECESARIOS PARA COPIAR A NUEVA MÁQUINA")
    print("="*80)
    print()
    
    print("✅ INCLUIR:")
    archivos_incluir = [
        "Todo el código fuente (apps: autenticacion/, maestros/, ventas/, etc.)",
        "config/settings.py (editar credenciales de BD)",
        "requirements.txt",
        "manage.py",
        "Todos los scripts .py de la raíz",
        "Toda la documentación .md",
        "instalar.ps1 / instalar.sh",
        ".gitignore",
    ]
    
    for item in archivos_incluir:
        print(f"  ✓ {item}")
    
    print()
    print("❌ NO INCLUIR:")
    archivos_excluir = [
        "env/ (entorno virtual - crear nuevo en cada máquina)",
        "db.sqlite3 (si existe)",
        "__pycache__/ (archivos compilados)",
        "*.pyc (archivos compilados)",
        ".vscode/ (configuración de IDE)",
        "logs/ (archivos de log)",
        ".env (credenciales - crear nuevo)",
    ]
    
    for item in archivos_excluir:
        print(f"  ✗ {item}")
    
    print()
    print("="*80)
    print(" 📦 ORDEN DE EJECUCIÓN EN NUEVA MÁQUINA")
    print("="*80)
    print()
    
    pasos = [
        "1. Copiar archivos del proyecto",
        "2. Instalar Python 3.13+",
        "3. Instalar MySQL 8.0+",
        "4. Crear base de datos MySQL",
        "5. Editar config/settings.py con credenciales",
        "6. Ejecutar script de instalación (instalar.ps1 o instalar.sh)",
        "7. O manualmente:",
        "   - python -m venv env",
        "   - Activar entorno",
        "   - pip install -r requirements.txt",
        "   - python manage.py migrate",
        "   - Ejecutar scripts de corrección",
        "   - python seed_simple.py",
        "   - python configurar_permisos_vendedor.py",
        "8. python verify_setup.py (verificar)",
        "9. python manage.py runserver (iniciar)",
        "10. Acceder a http://127.0.0.1:8000/admin/",
    ]
    
    for paso in pasos:
        print(f"  {paso}")
    
    print()
    print("="*80)
    print(" ✅ DOCUMENTACIÓN LISTA")
    print("="*80)
    print()
    
    # Generar archivo de resumen
    resumen_file = "RESUMEN_INSTALACION.txt"
    with open(resumen_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write(" RESUMEN DE INSTALACIÓN - DULCERÍA LILIS\n")
        f.write("="*80 + "\n\n")
        f.write(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("PASOS RÁPIDOS:\n")
        f.write("-" * 80 + "\n")
        f.write("1. Copiar proyecto a nueva máquina\n")
        f.write("2. Instalar Python 3.13+ y MySQL 8.0+\n")
        f.write("3. Crear BD: CREATE DATABASE empresa_lilis;\n")
        f.write("4. Editar config/settings.py con credenciales\n")
        f.write("5. Ejecutar: .\\instalar.ps1 (Windows) o ./instalar.sh (Linux)\n")
        f.write("6. Verificar: python verify_setup.py\n")
        f.write("7. Iniciar: python manage.py runserver\n\n")
        
        f.write("CREDENCIALES POR DEFECTO:\n")
        f.write("-" * 80 + "\n")
        f.write("Admin: admin / admin123\n")
        f.write("Vendedor: vendedor1 / vendedor123\n")
        f.write("Bodeguero: bodeguero1 / bodeguero123\n")
        f.write("Gerente: gerente / gerente123\n\n")
        
        f.write("DOCUMENTACIÓN:\n")
        f.write("-" * 80 + "\n")
        for archivo, descripcion in archivos_documentacion:
            f.write(f"{archivo:<35} - {descripcion}\n")
        
        f.write("\nVer INSTRUCTIVO_INSTALACION.md para detalles completos.\n")
    
    print(f"📄 Archivo creado: {resumen_file}")
    print()
    print("Usa este archivo como referencia rápida para instalar en otra máquina.")
    print()

if __name__ == '__main__':
    main()
