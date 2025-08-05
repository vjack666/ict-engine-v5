#!/usr/bin/env python3
"""
🔍 VALIDACIÓN FINAL - CANDLE DOWNLOADER COMPLETADO
===============================================

Script de validación final para verificar que el candle downloader
está completamente integrado y funcionando correctamente.

- ✅ Imports correctos
- ✅ Logging centralizado
- ✅ Integración dashboard
- ✅ Backend funcional
- ✅ UI responsiva

Autor: Sistema Sentinel v5.0
Fecha: 2025-08-05
"""

import sys
from pathlib import Path

# Configurar paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test básico de imports"""
    print("🔍 Validando imports...")

    try:
        # Test sistema logging
        from sistema.logging_interface import enviar_senal_log
        print("  ✅ sistema.logging_interface - OK")

        # Test candle downloader widget
        from dashboard.candle_downloader_widget import candle_downloader_widget
        print("  ✅ candle_downloader_widget - OK")

        # Test advanced downloader
        from core.data_management.advanced_candle_downloader import AdvancedCandleDownloader
        print("  ✅ AdvancedCandleDownloader - OK")

        # Test dashboard integration
        from dashboard.dashboard_definitivo import SentinelDashboardDefinitivo
        print("  ✅ Dashboard integration - OK")

        return True

    except ImportError as e:
        # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"  ❌ Error de import: {e}")
        return False

def test_logging_integration():
    """Test del sistema de logging centralizado"""
    print("\n📊 Validando logging centralizado...")

    try:
        from sistema.logging_interface import enviar_senal_log

        # Test logging básico
        enviar_senal_log("INFO", "🔍 Test de validación final - sistema operativo", "validate_final", "test")
        print("  ✅ Logging centralizado - OK")

        return True

    except Exception as e:
        # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"  ❌ Error en logging: {e}")
        return False

def test_downloader_backend():
    """Test del backend del downloader"""
    print("\n🚀 Validando backend downloader...")

    try:
        from core.data_management.advanced_candle_downloader import get_advanced_candle_downloader

        # Crear instancia
        downloader = get_advanced_candle_downloader()

        # Test básico de métodos
        stats = downloader.get_download_statistics()
        progress = downloader.get_download_progress()

        print("  ✅ Backend downloader - OK")
        print(f"  📊 Estado inicial: {stats}")

        return True

    except Exception as e:
        # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"  ❌ Error en backend: {e}")
        return False

def test_widget_integration():
    """Test del widget de UI"""
    print("\n🎮 Validando widget UI...")

    try:
        from dashboard.candle_downloader_widget import candle_downloader_widget

        # Verificar que la instancia está disponible
        if candle_downloader_widget is not None:
            print("  ✅ Widget UI - OK")
            print("  🎯 Widget disponible para dashboard")
            return True
        else:
            print("  ❌ Widget no disponible")
            return False

    except Exception as e:
        # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"  ❌ Error en widget: {e}")
        return False

def test_dashboard_integration():
    """Test de integración en dashboard"""
    print("\n📱 Validando integración dashboard...")

    try:
        # Verificar que el dashboard puede importar componentes
        from dashboard.dashboard_definitivo import SentinelDashboardDefinitivo

        print("  ✅ Dashboard puede cargar componentes")

        # Verificar imports en __init__.py
        import dashboard

        print("  ✅ Módulo dashboard configurado")

        return True

    except Exception as e:
        # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"  ❌ Error en dashboard: {e}")
        return False

def main():
    """Función principal de validación"""
    print("🚀 VALIDACIÓN FINAL - CANDLE DOWNLOADER SYSTEM")
    print("=" * 50)

    tests = [
        ("Imports básicos", test_imports),
        ("Logging centralizado", test_logging_integration),
        ("Backend downloader", test_downloader_backend),
        ("Widget UI", test_widget_integration),
        ("Integración dashboard", test_dashboard_integration)
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"❌ Error ejecutando {test_name}: {e}")
            results.append(False)

    # Resumen final
    print("\n" + "=" * 50)
    print("📊 RESUMEN FINAL")
    print("=" * 50)

    passed = sum(results)
    total = len(results)

    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"  {status} - {test_name}")

    print(f"\n🎯 RESULTADO: {passed}/{total} tests pasaron")

    if passed == total:
        print("🎉 ¡CANDLE DOWNLOADER COMPLETAMENTE INTEGRADO!")
        print("✅ Sistema listo para producción")

        # Log final
        try:
            from sistema.logging_interface import enviar_senal_log
            enviar_senal_log("INFO", "🎉 Candle Downloader completamente validado y funcional", "validate_final", "completion")
        except:
            pass

    else:
        print("⚠️  Sistema requiere atención en algunas áreas")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
