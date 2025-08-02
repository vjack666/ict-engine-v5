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

    print("🔍 DIAGNÓSTICO DETALLADO DEL DASHBOARD")
    print("=" * 50)

    # Paso 1: Verificar que el archivo existe
    dashboard_file = project_root / "dashboard" / "dashboard_definitivo.py"
    print(f"📁 Archivo dashboard: {dashboard_file}")
    print(f"✅ Existe: {dashboard_file.exists()}")

    # Paso 2: Verificar imports individuales
    print(f"\n🔧 VERIFICANDO IMPORTS INDIVIDUALES:")

    try:
        print("   Importando textual...")
        from textual.app import App
        print("   ✅ textual - OK")
    except ImportError as e:
        print(f"   ❌ textual - ERROR: {e}")
        return

    try:
        print("   Importando rich...")
        from rich.console import Console
        print("   ✅ rich - OK")
    except ImportError as e:
        print(f"   ❌ rich - ERROR: {e}")
        return

    try:
        print("   Importando sistema.logging_interface...")
        from sistema.logging_interface import enviar_senal_log
        print("   ✅ sistema.logging_interface - OK")
    except ImportError as e:
        print(f"   ❌ sistema.logging_interface - ERROR: {e}")
        return

    try:
        print("   Importando core.ict_engine.veredicto_engine_v4...")
        from core.ict_engine.veredicto_engine_v4 import VeredictoEngine
        print("   ✅ core.ict_engine.veredicto_engine_v4.VeredictoEngine - OK")
    except ImportError as e:
        print(f"   ❌ core.ict_engine.veredicto_engine_v4.VeredictoEngine - ERROR: {e}")
        return

    # Paso 3: Intentar importar el dashboard completo
    print(f"\n🎯 IMPORTANDO DASHBOARD COMPLETO:")
    try:
        print("   Ejecutando import dashboard.dashboard_definitivo...")
        import dashboard.dashboard_definitivo
        print("   ✅ dashboard.dashboard_definitivo módulo - OK")

        print("   Accediendo a SentinelDashboardDefinitivo...")
        SentinelDashboardDefinitivo = dashboard.dashboard_definitivo.SentinelDashboardDefinitivo
        print("   ✅ SentinelDashboardDefinitivo clase - OK")

        print("   Creando instancia...")
        app = SentinelDashboardDefinitivo()
        print("   ✅ Instancia creada - OK")

    except Exception as e:
        print(f"   ❌ ERROR en dashboard: {e}")
        print(f"   📝 Tipo de error: {type(e)}")
        import traceback
        traceback.print_exc()
        return

    print(f"\n✅ TODOS LOS TESTS PASARON - EL DASHBOARD ESTÁ OK")

if __name__ == "__main__":
    test_dashboard_step_by_step()
