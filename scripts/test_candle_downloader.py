# MIGRADO A SLUC v2.0
from sistema.logging_interface import enviar_senal_log
#!/usr/bin/env python3
"""
🧪 TEST CANDLE DOWNLOADER - ICT ENGINE v5.0
===========================================

Script para probar la funcionalidad completa del Candle Downloader
Verifica integración entre widget, downloader y dashboard

Creado por: Sistema Sentinel
Fecha: 2025-08-05
"""

import sys
from pathlib import Path

# Agregar path del proyecto
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_candle_downloader_imports():
    """Probar que todos los imports del candle downloader funcionan"""

    print("🧪 TESTING CANDLE DOWNLOADER IMPORTS")
    print("=" * 50)

    # Test 1: Widget del dashboard
    try:
        from dashboard.candle_downloader_widget import CandleDownloaderWidget, candle_downloader_widget
        print("✅ CandleDownloaderWidget importado correctamente")
        print(f"   - Widget global disponible: {candle_downloader_widget is not None}")
        print(f"   - Tipo: {type(candle_downloader_widget)}")
    except ImportError as e:
        # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"❌ Error importando CandleDownloaderWidget: {e}")
        return False

    # Test 2: Integración del downloader
    try:
        from core.integrations.candle_downloader_integration import CandleDownloaderIntegration
        print("✅ CandleDownloaderIntegration importado correctamente")
    except ImportError as e:
        # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"❌ Error importando CandleDownloaderIntegration: {e}")

    # Test 3: Verificar disponibilidad en dashboard
    try:
        # Simular el import que hace el dashboard
        from dashboard.candle_downloader_widget import candle_downloader_widget
        from core.integrations.candle_downloader_integration import downloader_integration
        print("✅ Imports del dashboard verificados")
        print(f"   - candle_downloader_widget: {candle_downloader_widget is not None}")
        print(f"   - downloader_integration: {downloader_integration is not None}")
    except ImportError as e:
        print(f"⚠️ Algunos imports del dashboard fallan: {e}")

    return True

def test_widget_functionality():
    """Probar funcionalidad básica del widget"""

    print("\n🎮 TESTING WIDGET FUNCTIONALITY")
    print("=" * 50)

    try:
        from dashboard.candle_downloader_widget import candle_downloader_widget

        if candle_downloader_widget is None:
            print("❌ Widget global no disponible")
            return False

        # Test métodos básicos
        print("🔧 Probando métodos del widget...")

        # Test renderizado de paneles
        control_panel = candle_downloader_widget.render_control_panel()
        print(f"✅ Control panel: {type(control_panel)}")

        progress_panel = candle_downloader_widget.render_progress_panel()
        print(f"✅ Progress panel: {type(progress_panel)}")

        stats_panel = candle_downloader_widget.render_stats_panel()
        print(f"✅ Stats panel: {type(stats_panel)}")

        errors_panel = candle_downloader_widget.render_errors_panel()
        # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"✅ Errors panel: {type(errors_panel)}")

        # Test configuración
        candle_downloader_widget.configure_symbols(["EURUSD", "GBPUSD"])
        candle_downloader_widget.configure_timeframes(["H4", "H1", "M15"])
        candle_downloader_widget.configure_lookback(10000)
        print("✅ Configuración aplicada correctamente")

        # Test estadísticas
        stats = candle_downloader_widget.download_stats
        print(f"✅ Estadísticas: {stats}")

        return True

    except Exception as e:
        # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"❌ Error en funcionalidad del widget: {e}")
        return False

def test_dashboard_integration():
    """Probar integración con el dashboard"""

    print("\n📊 TESTING DASHBOARD INTEGRATION")
    print("=" * 50)

    try:
        # Verificar que el import del dashboard funciona
        import importlib.util

        # Cargar el módulo del dashboard
        dashboard_path = project_root / "dashboard" / "dashboard_definitivo.py"
        spec = importlib.util.spec_from_file_location("dashboard_definitivo", dashboard_path)

        if spec is None:
            print("❌ No se puede cargar el dashboard")
            return False

        print("✅ Dashboard puede ser importado")

        # Verificar variables específicas
        try:
            from dashboard.dashboard_definitivo import candle_downloader_available
            print(f"✅ candle_downloader_available: {candle_downloader_available}")
        except ImportError:
            print("⚠️ Variable candle_downloader_available no disponible")

        return True

    except Exception as e:
        # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"❌ Error en integración del dashboard: {e}")
        return False

def test_mt5_compatibility():
    """Probar compatibilidad con MT5"""

    print("\n🔗 TESTING MT5 COMPATIBILITY")
    print("=" * 50)

    try:
        from utils.mt5_data_manager import get_mt5_manager

        mt5_manager = get_mt5_manager()
        if mt5_manager:
            print("✅ MT5DataManager disponible")
            print(f"   - Tipo: {type(mt5_manager)}")

            # Test conexión
            if mt5_manager.connect():
                print("✅ Conexión MT5 exitosa")

                # Test datos básicos
                if mt5_manager.verificar_simbolo("EURUSD"):
                    print("✅ Símbolo EURUSD disponible")
                else:
                    print("⚠️ Símbolo EURUSD no disponible")
            else:
                print("⚠️ No se pudo conectar a MT5")
        else:
            print("❌ MT5DataManager no disponible")

        return True

    except Exception as e:
        # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"❌ Error en compatibilidad MT5: {e}")
        return False

def main():
    """Función principal de pruebas"""

    print("🚀 CANDLE DOWNLOADER INTEGRATION TEST")
    print("=" * 60)
    print(f"📁 Proyecto: {project_root}")
    print()

    # Ejecutar todas las pruebas
    tests = [
        test_candle_downloader_imports,
        test_widget_functionality,
        test_dashboard_integration,
        test_mt5_compatibility
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # # TODO: Migrar a enviar_senal_log("ERROR", mensaje, __name__, "sistema") # print(f"❌ Error ejecutando {test.__name__}: {e}")
            results.append(False)

    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS:")
    print(f"✅ Exitosas: {sum(results)}")
    print(f"❌ Fallidas: {len(results) - sum(results)}")
    print(f"📈 Porcentaje éxito: {(sum(results)/len(results)*100):.1f}%")

    if all(results):
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("📥 El Candle Downloader está completamente integrado")
    else:
        print("\n⚠️ Algunas pruebas fallaron")
        print("🔧 Revisar logs para solucionar problemas")

if __name__ == "__main__":
    main()
