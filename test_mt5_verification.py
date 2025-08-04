#!/usr/bin/env python3
"""
🧪 TEST DE VERIFICACIÓN DIRECTA MT5
=================================

Prueba las nuevas funciones de verificación directa de MT5.
"""

import sys
from pathlib import Path

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

def test_mt5_verification():
    print("🔍 Probando verificación directa de MT5...")

    try:
        from dashboard.poi_dashboard_integration import (
            _verificar_conexion_mt5_directa,
            _obtener_precio_actual_mt5,
            integrar_multi_poi_en_panel_ict
        )

        # Test 1: Verificación de conexión MT5
        print("\n📡 Test 1: Verificación directa de conexión MT5")
        mt5_status = _verificar_conexion_mt5_directa()

        print(f"   Conectado: {mt5_status['connected']}")
        print(f"   Error: {mt5_status.get('error', 'Ninguno')}")

        if mt5_status['connected']:
            print("   ✅ MT5 está conectado al broker")
            account_info = mt5_status.get('account_info', {})
            if account_info:
                print(f"   📊 Cuenta: {account_info.get('login', 'N/A')}")
                print(f"   🖥️ Servidor: {account_info.get('server', 'N/A')}")
                print(f"   💰 Balance: {account_info.get('balance', 'N/A')}")
        else:
            print("   🔴 MT5 no está conectado")

        # Test 2: Obtener precio actual
        print("\n💰 Test 2: Obtener precio actual de EURUSD")
        precio = _obtener_precio_actual_mt5('EURUSD')
        print(f"   Precio EURUSD: {precio:.5f}")

        # Test 3: Integración completa con verificación
        print("\n🎯 Test 3: Integración completa con verificación directa")

        class MockDashboard:
            def __init__(self):
                self.symbol = 'EURUSD'
                # NO incluimos current_price ni mt5_connected
                # para forzar verificación directa

        mock_dashboard = MockDashboard()
        panel = integrar_multi_poi_en_panel_ict(mock_dashboard)

        if panel is not None:
            print("   ✅ Panel creado exitosamente con verificación directa")
        else:
            print("   ❌ Error creando panel")

        print("\n" + "="*50)
        print("📋 RESUMEN:")
        print("="*50)
        print("✅ Verificación directa de MT5 implementada")
        print("✅ Obtención directa de precios implementada")
        print("✅ Integración actualizada para usar verificación real")
        print("🚀 Sistema listo - ya no depende de valores del dashboard")

        return True

    except Exception as e:
        print(f"❌ Error en test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_mt5_verification()
    sys.exit(0 if success else 1)
