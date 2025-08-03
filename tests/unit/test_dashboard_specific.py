# 🔍 TEST ESPECÍFICO DEL DASHBOARD
# Diagnóstico detallado del problema de import

import sys
import os
from pathlib import Path

# Configurar path del proyecto
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def test_dashboard_step_by_step():
    """Test paso a paso del dashboard para encontrar el problema exacto"""

    enviar_senal_log("INFO", "🔍 DIAGNÓSTICO DETALLADO DEL DASHBOARD", "test_dashboard_specific", "migration")
    enviar_senal_log("INFO", "=" * 50, "test_dashboard_specific", "migration")

    # Paso 1: Verificar que el archivo existe
    dashboard_file = project_root / "dashboard" / "dashboard_definitivo.py"
    enviar_senal_log("INFO", f"📁 Archivo dashboard: {dashboard_file}", "test_dashboard_specific", "migration")
    enviar_senal_log("INFO", f"✅ Existe: {dashboard_file.exists(, "test_dashboard_specific", "migration")}")

    # Paso 2: Verificar imports individuales
    enviar_senal_log("INFO", f"\n🔧 VERIFICANDO IMPORTS INDIVIDUALES:", "test_dashboard_specific", "migration")

    try:
        enviar_senal_log("INFO", "   Importando textual...", "test_dashboard_specific", "migration")
        from textual.app import App
        enviar_senal_log("INFO", "   ✅ textual - OK", "test_dashboard_specific", "migration")
    except ImportError as e:
        enviar_senal_log("ERROR", f"   ❌ textual - ERROR: {e}", "test_dashboard_specific", "migration")
        return

    try:
        enviar_senal_log("INFO", "   Importando rich...", "test_dashboard_specific", "migration")
        from rich.console import Console
        enviar_senal_log("INFO", "   ✅ rich - OK", "test_dashboard_specific", "migration")
    except ImportError as e:
        enviar_senal_log("ERROR", f"   ❌ rich - ERROR: {e}", "test_dashboard_specific", "migration")
        return

    try:
        enviar_senal_log("INFO", "   Importando sistema.logging_interface...", "test_dashboard_specific", "migration")
        from sistema.logging_interface import enviar_senal_log
        enviar_senal_log("INFO", "   ✅ sistema.logging_interface - OK", "test_dashboard_specific", "migration")
    except ImportError as e:
        enviar_senal_log("ERROR", f"   ❌ sistema.logging_interface - ERROR: {e}", "test_dashboard_specific", "migration")
        return

    try:
        enviar_senal_log("INFO", "   Importando core.ict_engine.veredicto_engine_v4...", "test_dashboard_specific", "migration")
        from core.ict_engine.veredicto_engine_v4 import VeredictoEngine
        enviar_senal_log("INFO", "   ✅ core.ict_engine.veredicto_engine_v4.VeredictoEngine - OK", "test_dashboard_specific", "migration")
    except ImportError as e:
        enviar_senal_log("ERROR", f"   ❌ core.ict_engine.veredicto_engine_v4.VeredictoEngine - ERROR: {e}", "test_dashboard_specific", "migration")
        return

    # Paso 3: Intentar importar el dashboard completo
    enviar_senal_log("INFO", f"\n🎯 IMPORTANDO DASHBOARD COMPLETO:", "test_dashboard_specific", "migration")
    try:
        enviar_senal_log("INFO", "   Ejecutando import dashboard.dashboard_definitivo...", "test_dashboard_specific", "migration")
        import dashboard.dashboard_definitivo
        enviar_senal_log("INFO", "   ✅ dashboard.dashboard_definitivo módulo - OK", "test_dashboard_specific", "migration")

        enviar_senal_log("INFO", "   Accediendo a SentinelDashboardDefinitivo...", "test_dashboard_specific", "migration")
        SentinelDashboardDefinitivo = dashboard.dashboard_definitivo.SentinelDashboardDefinitivo
        enviar_senal_log("INFO", "   ✅ SentinelDashboardDefinitivo clase - OK", "test_dashboard_specific", "migration")

        enviar_senal_log("INFO", "   Creando instancia...", "test_dashboard_specific", "migration")
        app = SentinelDashboardDefinitivo()
        enviar_senal_log("INFO", "   ✅ Instancia creada - OK", "test_dashboard_specific", "migration")

    except Exception as e:
        enviar_senal_log("ERROR", f"   ❌ ERROR en dashboard: {e}", "test_dashboard_specific", "migration")
        enviar_senal_log("ERROR", f"   📝 Tipo de error: {type(e, "test_dashboard_specific", "migration")}")
        import traceback
        traceback.print_exc()
        return

    enviar_senal_log("INFO", f"\n✅ TODOS LOS TESTS PASARON - EL DASHBOARD ESTÁ OK", "test_dashboard_specific", "migration")

if __name__ == "__main__":
    test_dashboard_step_by_step()
