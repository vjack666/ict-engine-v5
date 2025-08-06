#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTING POI DASHBOARD INTEGRATION v2.0
========================================
Test aislado para verificar la integración POI
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("🚀 INICIANDO TESTING POI DASHBOARD INTEGRATION v2.0")
print("=" * 60)

try:
    # Test 1: Importar módulos del sistema
    print("📦 Test 1: Importando módulos del sistema...")
    from sistema.logging_interface import enviar_senal_log
    print("✅ sistema.logging_interface importado")

    from utils.mt5_data_manager import get_mt5_manager
    print("✅ utils.mt5_data_manager importado")

    from dashboard.dashboard_controller import get_dashboard_controller
    print("✅ dashboard.dashboard_controller importado")

    print("✅ Test 1 EXITOSO - Todos los módulos del sistema importados")

except Exception as e:
    print(f"❌ Test 1 FALLÓ - Error de importación: {e}")
    print("🔍 Verificando estructura de directorios...")
    print(f"📁 Directorio actual: {os.getcwd()}")
    print(f"📁 Directorio script: {os.path.dirname(os.path.abspath(__file__))}")
    print(f"📁 Python paths: {sys.path[:3]}...")
    exit(1)

try:
    # Test 2: Importar la integración POI
    print("\n📦 Test 2: Importando POI Dashboard Integration...")
    from dashboard.poi_dashboard_integration import integrar_multi_poi_en_panel_ict
    print("✅ poi_dashboard_integration importado exitosamente")

    print("✅ Test 2 EXITOSO - Integración POI disponible")

except Exception as e:
    print(f"❌ Test 2 FALLÓ - Error en POI Integration: {e}")
    import traceback
    print(f"🔍 Stack trace: {traceback.format_exc()}")
    exit(1)

try:
    # Test 3: Verificar sistemas básicos
    print("\n🔧 Test 3: Verificando sistemas básicos...")

    # Test MT5 Manager
    try:
        mt5_manager = get_mt5_manager()
        mt5_status = "🟢 Disponible" if mt5_manager else "🔴 No disponible"
        print(f"📊 MT5 Manager: {mt5_status}")
    except Exception as e:
        print(f"⚠️ MT5 Manager: Error - {e}")

    # Test Dashboard Controller
    try:
        controller = get_dashboard_controller()
        controller_status = "🟢 Disponible" if controller else "🔴 No disponible"
        print(f"🎛️ Dashboard Controller: {controller_status}")
    except Exception as e:
        print(f"⚠️ Dashboard Controller: Error - {e}")

    # Test Logging
    try:
        enviar_senal_log("INFO", "🧪 Test de logging desde POI Integration Test", "poi_test", "testing")
        print("📝 SLUC Logging: ✅ Funcionando")
    except Exception as e:
        print(f"⚠️ SLUC Logging: Error - {e}")

    print("✅ Test 3 COMPLETADO - Verificación de sistemas básicos")

except Exception as e:
    print(f"❌ Test 3 FALLÓ - Error en verificación de sistemas: {e}")

try:
    # Test 4: Simulación de integración POI
    print("\n🎯 Test 4: Simulación de integración POI...")

    # Crear un dashboard_instance simulado
    class MockDashboardInstance:
        def __init__(self):
            self.real_market_data = {
                'H1': {'open': [1.1000, 1.1010], 'high': [1.1020, 1.1030], 'low': [0.9990, 1.0995], 'close': [1.1010, 1.1020]},
                'H4': {'open': [1.0990, 1.1005], 'high': [1.1015, 1.1025], 'low': [0.9980, 1.0990], 'close': [1.1005, 1.1015]}
            }

    mock_dashboard = MockDashboardInstance()
    print("📊 Mock dashboard instance creado")

    # Intentar la integración POI con debug
    try:
        print("🔍 Iniciando integración POI...")
        resultado = integrar_multi_poi_en_panel_ict(mock_dashboard, 'H1')
        print(f"🎯 Resultado de integración: {type(resultado)}")

        if hasattr(resultado, 'title'):
            print(f"📋 Tabla creada con título: {getattr(resultado, 'title', 'Sin título')}")

        print("✅ Test 4 EXITOSO - Integración POI simulada completada")

    except Exception as e:
        print(f"❌ Test 4 ERROR ESPECÍFICO: {e}")
        import traceback
        print("🔍 Stack trace completo:")
        print(traceback.format_exc())

except Exception as e:
    print(f"❌ Test 4 FALLÓ - Error en integración POI: {e}")
    import traceback
    print(f"🔍 Stack trace completo:")
    print(traceback.format_exc())

print("\n" + "=" * 60)
print("🎉 TESTING POI DASHBOARD INTEGRATION COMPLETADO")
print("📊 Revisa los resultados arriba para verificar el estado")
print("=" * 60)
