#!/usr/bin/env python3
"""
🎯 ACTIVADOR DEL CORRECTOR DE IMPORTS
===================================

Script de activación para el corrector automático de imports no utilizados.
Proporciona diferentes modos de ejecución y opciones de corrección.

Autor: Sistema Sentinel Grid
Fecha: 2025-08-06
Versión: v1.0
"""

from sistema.sic import os
from sistema.sic import sys
from sistema.sic import Path

# Agregar el directorio scripts al path para importar el corrector
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

try:
    from fix_unused_imports import UnusedImportDetector
except ImportError as e:
    print(f"❌ Error importando el corrector: {e}")
    sys.exit(1)

def show_banner():
    """Muestra el banner del programa"""
    print("🎯" + "=" * 58 + "🎯")
    print("🚀         CORRECTOR DE IMPORTS NO UTILIZADOS         🚀")
    print("🎯" + "=" * 58 + "🎯")
    print("")

def show_menu():
    """Muestra el menú principal"""
    print("OPCIONES DISPONIBLES:")
    print("1. 🔍 Análisis completo (solo mostrar)")
    print("2. 🧪 Dry-run (mostrar qué se corregiría)")
    print("3. ✅ Corrección automática (con backup)")
    print("4. 🎯 Corrección del archivo actual")
    print("5. 📊 Solo generar reporte")
    print("0. ❌ Salir")
    print("")

def get_project_root():
    """Obtiene la ruta raíz del proyecto"""
    # El script está en scripts/, así que subimos un nivel
    return Path(__file__).parent.parent

def run_analysis_only():
    """Ejecuta solo el análisis sin correcciones"""
    print("🔍 EJECUTANDO ANÁLISIS COMPLETO")
    print("-" * 40)

    project_root = get_project_root()
    detector = UnusedImportDetector(str(project_root))
    detector.run_analysis(fix_files=False, dry_run=False)

def run_dry_run():
    """Ejecuta dry-run para mostrar qué se corregiría"""
    print("🧪 EJECUTANDO DRY-RUN")
    print("-" * 40)

    project_root = get_project_root()
    detector = UnusedImportDetector(str(project_root))
    detector.run_analysis(fix_files=True, dry_run=True)

def run_auto_fix():
    """Ejecuta la corrección automática con backup"""
    print("⚠️  CORRECCIÓN AUTOMÁTICA CON BACKUP")
    print("-" * 40)
    print("Esta opción corregirá automáticamente todos los archivos.")
    print("Se crearán backups de los archivos modificados.")
    print("")

    response = input("¿Continuar? (s/N): ").lower().strip()
    if response not in ['s', 'si', 'sí', 'yes', 'y']:
        print("❌ Operación cancelada")
        return

    project_root = get_project_root()
    detector = UnusedImportDetector(str(project_root))
    detector.run_analysis(fix_files=True, dry_run=False)

def fix_current_file():
    """Corrige el archivo actual (live_only_config.py)"""
    print("🎯 CORRIGIENDO ARCHIVO ESPECÍFICO")
    print("-" * 40)

    current_file = get_project_root() / "config" / "live_only_config.py"

    if not current_file.exists():
        print(f"❌ Archivo no encontrado: {current_file}")
        return

    print(f"📄 Archivo: {current_file.relative_to(get_project_root())}")

    # Crear detector para un solo archivo
    detector = UnusedImportDetector(str(get_project_root()))
    analysis = detector.analyze_file(current_file)

    if not analysis.unused_imports:
        print("✅ No se encontraron imports no utilizados en este archivo")
        return

    print(f"🔴 Imports no utilizados encontrados: {len(analysis.unused_imports)}")
    for imp in analysis.unused_imports:
        print(f"   - Línea {imp.line_number}: {imp.line_content.strip()}")

    print("")
    response = input("¿Corregir este archivo? (s/N): ").lower().strip()
    if response not in ['s', 'si', 'sí', 'yes', 'y']:
        print("❌ Operación cancelada")
        return

    if detector.fix_file(analysis, dry_run=False):
        print("✅ Archivo corregido exitosamente")
    else:
        print("❌ Error corrigiendo el archivo")

def generate_report_only():
    """Genera solo el reporte sin hacer correcciones"""
    print("📊 GENERANDO REPORTE DETALLADO")
    print("-" * 40)

    project_root = get_project_root()
    detector = UnusedImportDetector(str(project_root))

    # Ejecutar análisis sin correcciones
    detector.run_analysis(fix_files=False, dry_run=False)

def main():
    """Función principal del activador"""
    show_banner()

    # Verificar que estamos en el directorio correcto
    project_root = get_project_root()
    if not (project_root / "config" / "live_only_config.py").exists():
        print("❌ No se encuentra el archivo live_only_config.py")
        print(f"   Directorio actual: {project_root}")
        print("   Asegúrate de ejecutar este script desde el directorio correcto")
        return

    print(f"📁 Proyecto: {project_root.name}")
    print(f"📍 Ruta: {project_root}")
    print("")

    while True:
        show_menu()

        try:
            choice = input("Selecciona una opción (0-5): ").strip()
            print("")

            if choice == "0":
                print("👋 ¡Hasta luego!")
                break
            elif choice == "1":
                run_analysis_only()
            elif choice == "2":
                run_dry_run()
            elif choice == "3":
                run_auto_fix()
            elif choice == "4":
                fix_current_file()
            elif choice == "5":
                generate_report_only()
            else:
                print("❌ Opción no válida. Por favor selecciona 0-5.")

            print("")
            input("Presiona Enter para continuar...")
            print("\n" + "="*60 + "\n")

        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            print("Por favor intenta de nuevo.")

if __name__ == "__main__":
    main()
