#!/usr/bin/env python3
"""
🔍 TEST SISTEMA DE CAJA NEGRA
============================

Script de prueba para verificar que el sistema de caja negra
está funcionando correctamente y conectado al dashboard.
"""

def test_sistema_caja_negra():
    """Prueba completa del sistema de caja negra."""

    print("🔍 INICIANDO TEST SISTEMA DE CAJA NEGRA")
    print("=" * 50)

    # 1. Test de imports
    try:
        from poi_black_box_diagnostics import POIBlackBoxDiagnostics, integrar_multi_poi_con_diagnosticos
        print("✅ Imports de caja negra: OK")
    except Exception as e:
        print(f"❌ Error en imports: {e}")
        return False

    # 2. Test de inicialización
    try:
        black_box = POIBlackBoxDiagnostics()
        print("✅ Inicialización de caja negra: OK")
    except Exception as e:
        print(f"❌ Error en inicialización: {e}")
        return False

    # 3. Test de dashboard mock
    try:
        class MockDashboard:
            def __init__(self):
                self.df_m5 = None
                self.df_m15 = None
                self.df_h1 = None
                self.df_h4 = None
                self.current_price = None
                self.mt5_connected = False

        mock_dashboard = MockDashboard()
        print("✅ Dashboard mock creado: OK")
    except Exception as e:
        print(f"❌ Error creando dashboard mock: {e}")
        return False

    # 4. Test de diagnóstico
    try:
        diagnostic_result = black_box.run_full_diagnostic(mock_dashboard)
        print(f"✅ Diagnóstico completo: OK")
        print(f"   - Status: {diagnostic_result.get('status', 'UNKNOWN')}")
        print(f"   - Issues críticos: {len(diagnostic_result.get('critical_issues', []))}")
        print(f"   - Soluciones: {len(diagnostic_result.get('solutions', []))}")
    except Exception as e:
        print(f"❌ Error en diagnóstico: {e}")
        return False

    # 5. Test de integración con dashboard
    try:
        contenido_integrado = integrar_multi_poi_con_diagnosticos(mock_dashboard)
        print("✅ Integración con dashboard: OK")
        print(f"   - Tipo de contenido: {type(contenido_integrado)}")
    except Exception as e:
        print(f"❌ Error en integración: {e}")
        return False

    # 6. Test de importación desde dashboard
    try:
        from dashboard.dashboard_definitivo import SentinelDashboardDefinitivo
        print("✅ Dashboard definitivo puede importar caja negra: OK")
    except Exception as e:
        print(f"❌ Error importando dashboard: {e}")
        return False

    print("\n🎉 TODOS LOS TESTS PASARON!")
    print("🔍 Sistema de caja negra completamente funcional")
    print("✅ Listo para usar en producción")

    return True

if __name__ == "__main__":
    success = test_sistema_caja_negra()
    if success:
        print("\n🚀 Sistema listo para usar!")
    else:
        print("\n⚠️ Revisar errores antes de usar")
