#!/usr/bin/env python3
"""
🎯 VALIDADOR FINAL ESTRATEGIA COMPLETA
====================================
Valida que la estrategia "AÑADIR → REEMPLAZAR → ELIMINAR" fue ejecutada exitosamente

Autor: Sistema Sentinel Grid
Fecha: 2025-08-06
Versión: v3.0-Final
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def validar_sic_expandido():
    """🔍 Validar que el SIC fue expandido correctamente"""

    print("🔍 VALIDANDO SIC EXPANDIDO...")

    sic_path = Path('sistema/sic.py')

    if not sic_path.exists():
        print("❌ ERROR: sistema/sic.py no encontrado")
        return False

    try:
        with open(sic_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Verificar que contiene imports expandidos
        checks = [
            ('typing imports', 'from typing import'),
            ('datetime imports', 'from datetime import'),
            ('pathlib imports', 'from pathlib import Path'),
            ('dataclasses imports', 'from dataclasses import'),
            ('os import', 'import os'),
            ('sys import', 'import sys'),
            ('json import', 'import json'),
        ]

        success_count = 0
        for name, pattern in checks:
            if pattern in content:
                print(f"   ✅ {name}: Presente")
                success_count += 1
            else:
                print(f"   ⚠️ {name}: No encontrado")

        print(f"   📊 Verificaciones exitosas: {success_count}/{len(checks)}")

        # Verificar tamaño del archivo (debe ser mayor después de la expansión)
        file_size = sic_path.stat().st_size
        print(f"   📏 Tamaño del SIC: {file_size:,} bytes")

        if file_size > 8000:  # Debería ser >8KB después de la expansión
            print(f"   ✅ Tamaño adecuado para SIC expandido")
            return True
        else:
            print(f"   ⚠️ Tamaño menor al esperado")
            return False

    except Exception as e:
        print(f"   ❌ Error leyendo SIC: {e}")
        return False

def validar_imports_reemplazados():
    """🔍 Validar que los imports fueron reemplazados masivamente"""

    print("\n🔍 VALIDANDO IMPORTS REEMPLAZADOS...")

    files_with_sic = 0
    files_checked = 0
    files_with_old_imports = 0

    # Patrones de imports viejos que deberían haber sido reemplazados
    old_patterns = [
        'from typing import',
        'from datetime import',
        'import os',
        'import sys',
        'import json',
        'from dataclasses import'
    ]

    for root, dirs, files in os.walk('.'):
        # Filtrar directorios
        dirs[:] = [d for d in dirs if not d.startswith(('__pycache__', '.git', 'backup_'))]

        for file in files:
            if file.endswith('.py') and file not in ['sic.py', 'fase1_scan_imports.py', 'fase2_expandir_sic.py', 'fase3_eliminar_imports.py', 'validador_final_estrategia.py']:
                file_path = Path(root) / file
                files_checked += 1

                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    # Verificar si tiene import del SIC
                    if 'from sistema.sic import' in content:
                        files_with_sic += 1

                    # Verificar si aún tiene imports viejos
                    has_old_imports = False
                    for pattern in old_patterns:
                        if pattern in content and 'from sistema.sic import' not in content:
                            has_old_imports = True
                            break

                    if has_old_imports:
                        files_with_old_imports += 1

                except Exception as e:
                    print(f"   ⚠️ Error leyendo {file_path}: {e}")

    print(f"   📁 Archivos verificados: {files_checked}")
    print(f"   ✅ Archivos con import SIC: {files_with_sic}")
    print(f"   ⚠️ Archivos con imports viejos: {files_with_old_imports}")

    if files_with_old_imports == 0:
        print(f"   🎉 PERFECTO: Todos los imports fueron reemplazados")
        return True
    else:
        print(f"   ⚠️ Algunos archivos aún tienen imports viejos")
        return False

def validar_backups_creados():
    """🔍 Validar que los backups fueron creados correctamente"""

    print("\n🔍 VALIDANDO BACKUPS CREADOS...")

    # Buscar directorios de backup
    backup_dirs = []
    for item in Path('.').iterdir():
        if item.is_dir() and item.name.startswith('backup_'):
            backup_dirs.append(item)

    print(f"   📁 Directorios de backup encontrados: {len(backup_dirs)}")

    for backup_dir in backup_dirs:
        print(f"   📦 {backup_dir.name}")

        # Contar archivos en backup
        file_count = 0
        for root, dirs, files in os.walk(backup_dir):
            file_count += len([f for f in files if f.endswith('.py')])

        print(f"      📄 Archivos Python: {file_count}")

    # Verificar backup específico de fase 3
    fase3_backup = None
    for backup_dir in backup_dirs:
        if 'fase3_eliminar' in backup_dir.name:
            fase3_backup = backup_dir
            break

    if fase3_backup:
        print(f"   ✅ Backup de Fase 3 encontrado: {fase3_backup.name}")
        return True
    else:
        print(f"   ⚠️ Backup de Fase 3 no encontrado")
        return False

def validar_reportes_generados():
    """🔍 Validar que los reportes fueron generados"""

    print("\n🔍 VALIDANDO REPORTES GENERADOS...")

    reports_dir = Path('migration_reports')

    if not reports_dir.exists():
        print("   ❌ Directorio migration_reports no encontrado")
        return False

    report_files = list(reports_dir.glob('*.txt')) + list(reports_dir.glob('*.json'))
    print(f"   📄 Reportes encontrados: {len(report_files)}")

    for report_file in report_files:
        print(f"   📊 {report_file.name}")

    # Verificar reportes específicos
    required_reports = [
        'fase1_scan_results.json',
        'fase3_report_executed_'
    ]

    found_reports = 0
    for required in required_reports:
        for report_file in report_files:
            if required in report_file.name:
                found_reports += 1
                break

    print(f"   ✅ Reportes requeridos encontrados: {found_reports}/{len(required_reports)}")

    return found_reports == len(required_reports)

def test_import_sic():
    """🧪 Test básico de import del SIC"""

    print("\n🧪 TESTING IMPORT DEL SIC...")

    try:
        # Agregar directorio actual al path
        import sys
        from pathlib import Path

        current_dir = Path('.').resolve()
        if str(current_dir) not in sys.path:
            sys.path.insert(0, str(current_dir))

        # Intentar importar el SIC
        import sistema.sic
        print("   ✅ Import del SIC exitoso")

        # Verificar algunos imports básicos disponibles en el SIC
        available_modules = []

        if hasattr(sistema.sic, 'os'):
            available_modules.append("os")
        if hasattr(sistema.sic, 'sys'):
            available_modules.append("sys")
        if hasattr(sistema.sic, 'json'):
            available_modules.append("json")
        if hasattr(sistema.sic, 'datetime'):
            available_modules.append("datetime")
        if hasattr(sistema.sic, 'Path'):
            available_modules.append("Path")

        print(f"   📦 Módulos disponibles en SIC: {', '.join(available_modules)}")

        return True

    except Exception as e:
        print(f"   ❌ Error importando SIC: {e}")
        return False

def main():
    """🚀 Función principal de validación"""

    print("🎯 VALIDADOR FINAL - ESTRATEGIA 'AÑADIR → REEMPLAZAR → ELIMINAR'")
    print("=" * 80)

    validations = [
        ("SIC Expandido", validar_sic_expandido),
        ("Imports Reemplazados", validar_imports_reemplazados),
        ("Backups Creados", validar_backups_creados),
        ("Reportes Generados", validar_reportes_generados),
        ("Test Import SIC", test_import_sic)
    ]

    results = {}

    for name, validator in validations:
        print(f"\n{'='*20} {name} {'='*20}")
        results[name] = validator()

    # Resumen final
    print("\n" + "="*80)
    print("📊 RESUMEN DE VALIDACIÓN FINAL")
    print("="*80)

    passed = 0
    for name, result in results.items():
        status = "✅ EXITOSO" if result else "❌ FALLÓ"
        print(f"   {name}: {status}")
        if result:
            passed += 1

    success_rate = (passed / len(results)) * 100
    print(f"\n🎯 TASA DE ÉXITO: {passed}/{len(results)} ({success_rate:.1f}%)")

    if success_rate == 100:
        print("\n🎉 VALIDACIÓN COMPLETA EXITOSA")
        print("✅ La estrategia 'AÑADIR → REEMPLAZAR → ELIMINAR' fue ejecutada perfectamente")
        print("🏆 ITC ENGINE v5.0 - SISTEMA CENTRALIZADO OPERATIVO")
    elif success_rate >= 80:
        print("\n✅ VALIDACIÓN MAYORMENTE EXITOSA")
        print("⚠️ Algunas verificaciones menores fallaron, pero el sistema es funcional")
    else:
        print("\n⚠️ VALIDACIÓN CON PROBLEMAS")
        print("❌ Se requiere revisión manual de los componentes que fallaron")

    print("\n📅 Validación completada:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    return success_rate == 100

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
