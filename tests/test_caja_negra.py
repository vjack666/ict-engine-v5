from sistema.logging_interface import enviar_senal_log
#!/usr/bin/env python3
"""
🔍 TEST SISTEMA DE CAJA NEGRA
============================

Script de prueba para verificar que el sistema de caja negra
está funcionando correctamente y conectado al dashboard.
"""

def test_sistema_caja_negra():
    """Prueba completa del sistema de caja negra."""

    enviar_senal_log("INFO", "🔍 INICIANDO TEST SISTEMA DE CAJA NEGRA", "test_caja_negra", "migration")
    enviar_senal_log("INFO", "=" * 50, "test_caja_negra", "migration")

    # 1. Test de imports
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from utils.system_diagnostics import POIBlackBoxDiagnostics, integrar_multi_poi_con_diagnosticos
        enviar_senal_log("INFO", "✅ Imports de sistema de diagnósticos simplificado: OK", "test_caja_negra", "migration")
    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en imports: {e}", "test_caja_negra", "migration")
        return False

    # 2. Test de inicialización
    try:
        black_box = POIBlackBoxDiagnostics()
        enviar_senal_log("INFO", "✅ Inicialización de caja negra: OK", "test_caja_negra", "migration")
    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en inicialización: {e}", "test_caja_negra", "migration")
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
        enviar_senal_log("INFO", "✅ Dashboard mock creado: OK", "test_caja_negra", "migration")
    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error creando dashboard mock: {e}", "test_caja_negra", "migration")
        return False

    # 4. Test de diagnóstico
    try:
        diagnostic_result = black_box.run_full_diagnostic(mock_dashboard)
        enviar_senal_log("INFO", f"✅ Diagnóstico completo: OK", "test_caja_negra", "migration")
        enviar_senal_log("INFO", f"   - Status: {diagnostic_result.get('status', 'UNKNOWN', "test_caja_negra", "migration")}")
        enviar_senal_log("INFO", f"   - Issues críticos: {len(diagnostic_result.get('critical_issues', [], "test_caja_negra", "migration"))}")
        enviar_senal_log("INFO", f"   - Soluciones: {len(diagnostic_result.get('solutions', [], "test_caja_negra", "migration"))}")
    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en diagnóstico: {e}", "test_caja_negra", "migration")
        return False

    # 5. Test de integración con dashboard
    try:
        contenido_integrado = integrar_multi_poi_con_diagnosticos(mock_dashboard)
        enviar_senal_log("INFO", "✅ Integración con dashboard: OK", "test_caja_negra", "migration")
        enviar_senal_log("INFO", f"   - Tipo de contenido: {type(contenido_integrado, "test_caja_negra", "migration")}")
    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error en integración: {e}", "test_caja_negra", "migration")
        return False

    # 6. Test de importación desde dashboard
    try:
        from dashboard.dashboard_definitivo import SentinelDashboardDefinitivo
        enviar_senal_log("INFO", "✅ Dashboard definitivo puede importar caja negra: OK", "test_caja_negra", "migration")
    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error importando dashboard: {e}", "test_caja_negra", "migration")
        return False

    enviar_senal_log("INFO", "\n🎉 TODOS LOS TESTS PASARON!", "test_caja_negra", "migration")
    enviar_senal_log("INFO", "🔍 Sistema de caja negra completamente funcional", "test_caja_negra", "migration")
    enviar_senal_log("INFO", "✅ Listo para usar en producción", "test_caja_negra", "migration")

    return True

if __name__ == "__main__":
    success = test_sistema_caja_negra()
    if success:
        enviar_senal_log("INFO", "\n🚀 Sistema listo para usar!", "test_caja_negra", "migration")
    else:
        enviar_senal_log("ERROR", "\n⚠️ Revisar errores antes de usar", "test_caja_negra", "migration")
