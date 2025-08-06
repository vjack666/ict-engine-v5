#!/usr/bin/env python3
"""
🔍 VALIDADOR FINAL DEL PROYECTO
===============================
Script para verificar el estado final después de la migración SIC v3.0
"""

# Configurar path del proyecto PRIMERO
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# MIGRACIÓN SIC v3.0 + SLUC v2.1
from sistema.sic import enviar_senal_log, log_info, log_warning

from sistema.sic import sys
from sistema.sic import os

# Configurar path
# Ya configurado arriba
# current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.dirname(current_dir)
# sys.path.insert(0, project_root)

def test_sic_basic():
    """Prueba básica del SIC."""
    try:
        from sistema.sic import get_sic_status
        status = get_sic_status()
        print(f"✅ SIC v{status['version']} funcionando")
        print(f"   Exports: {status['total_exports']}")
        print(f"   Logging: {status['logging_available']}")
        enviar_senal_log("INFO", "Test de validación", "validador")
        return True
    except Exception as e:
        print(f"❌ Error en SIC: {e}")
        return False

def test_logging_system():
    """Prueba el sistema de logging."""
    try:
        from sistema.sic import get_smart_stats
        enviar_senal_log("INFO", "Test del sistema de logging", "validador")
        stats = get_smart_stats()
        print(f"✅ Logging funcionando - Stats: {stats}")
        return True
    except Exception as e:
        print(f"❌ Error en logging: {e}")
        return False

def test_critical_modules():
    """Prueba módulos críticos del proyecto."""
    modules_to_test = [
        "core.analytics.ict_analyzer",
        "utils.mt5_data_manager",
        "dashboard.problems_tab_renderer",
    ]

    results = {}
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✅ {module}")
            results[module] = True
        except Exception as e:
            print(f"❌ {module}: {e}")
            results[module] = False

    return results

def count_vs_code_errors():
    """Cuenta errores aproximados en archivos principales."""
    # Esta es una estimación basada en patterns comunes de error
    error_patterns = [
        "ModuleNotFoundError",
        "ImportError",
        "Cannot import",
        "is not defined"
    ]

    critical_files = [
        "dashboard/dashboard_definitivo.py",
        "core/analytics/ict_analyzer.py",
        "sistema/sic.py"
    ]

    total_lines_with_issues = 0
    for file_path in critical_files:
        full_path = os.path.join(project_root, file_path)
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for pattern in error_patterns:
                        total_lines_with_issues += content.count(pattern)
            except:
                pass

    return total_lines_with_issues

def main():
    print("🔍 VALIDACIÓN FINAL DEL PROYECTO ITC ENGINE v5.0")
    print("=" * 55)

    # Test básico del SIC
    sic_ok = test_sic_basic()

    # Test del sistema de logging
    logging_ok = test_logging_system()

    # Test de módulos críticos
    print("\n📋 MÓDULOS CRÍTICOS:")
    module_results = test_critical_modules()

    # Conteo aproximado de errores
    print(f"\n📊 ESTIMACIÓN DE ERRORES:")
    estimated_errors = count_vs_code_errors()
    print(f"   Patterns de error encontrados: {estimated_errors}")

    # Resumen final
    print("\n🎯 RESUMEN FINAL:")
    print(f"   SIC v3.0: {'✅' if sic_ok else '❌'}")
    print(f"   Logging: {'✅' if logging_ok else '❌'}")

    successful_modules = sum(1 for result in module_results.values() if result)
    total_modules = len(module_results)
    print(f"   Módulos OK: {successful_modules}/{total_modules}")

    if sic_ok and logging_ok and successful_modules >= total_modules * 0.7:
        print("\n🎉 MIGRACIÓN EXITOSA!")
        print("   El proyecto está listo para usarse.")
    else:
        print("\n⚠️  MIGRACIÓN PARCIAL")
        print("   Algunos componentes necesitan atención adicional.")

if __name__ == "__main__":
    main()
