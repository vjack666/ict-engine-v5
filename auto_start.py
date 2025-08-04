#!/usr/bin/env python3
"""
🤖 ICT ENGINE v5.0 - AUTO START
===============================

Script de inicio automático que lanza directamente el dashboard principal
sin menús interactivos.

Uso:
    python auto_start.py              # Dashboard directo
    python auto_start.py --debug      # Debug mode
    python auto_start.py --verbose    # Output detallado
"""

import sys
import os
from pathlib import Path

# 📁 Configurar paths del proyecto
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from sistema.logging_interface import enviar_senal_log

def auto_start_dashboard(debug_mode=False, verbose=False):
    """Inicia automáticamente el dashboard principal"""

    enviar_senal_log("INFO", "🤖 === ICT ENGINE v5.0 AUTO START ===", "auto_start", "startup")

    # 🚀 AUTO-DESCARGA INTELIGENTE
    try:
        from utils.mt5_data_manager import auto_download_essential_data

        enviar_senal_log("INFO", "📊 Iniciando auto-descarga de datos REALES...", "auto_start", "startup")

        success = auto_download_essential_data(
            symbols=["EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD"],
            timeframes=["H4", "H1", "M15", "M5", "M1"],
            lookback=30000
        )

        if success:
            enviar_senal_log("INFO", "✅ Datos REALES descargados exitosamente", "auto_start", "startup")
        else:
            enviar_senal_log("WARNING", "⚠️ Algunos datos no se descargaron - continuando...", "auto_start", "startup")

    except Exception as e:
        enviar_senal_log("WARNING", f"⚠️ Error en auto-descarga: {e}", "auto_start", "startup")

    # 🚀 LANZAR DASHBOARD AUTOMÁTICAMENTE
    try:
        enviar_senal_log("INFO", "🚀 Lanzando Dashboard Principal automáticamente...", "auto_start", "startup")

        from dashboard.dashboard_definitivo import SentinelDashboardDefinitivo

        # 🔧 Configurar ambiente
        if debug_mode:
            os.environ['TEXTUAL_DEBUG'] = '1'
            os.environ['TEXTUAL_CONSOLE'] = '1'
        if verbose:
            os.environ['TEXTUAL_LOG'] = '1'

        # 🎯 INICIAR DASHBOARD
        app = SentinelDashboardDefinitivo()
        enviar_senal_log("INFO", "✅ Dashboard iniciado - ¡Disfruta el trading!", "auto_start", "startup")
        app.run()

    except ImportError as e:
        enviar_senal_log("ERROR", f"❌ Error importando dashboard: {e}", "auto_start", "startup")
        enviar_senal_log("INFO", "🔧 Asegúrate de que todos los módulos estén instalados", "auto_start", "startup")
        return False
    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error inesperado: {e}", "auto_start", "startup")
        return False

    return True

def main():
    """Función principal de auto-start"""
    import argparse

    parser = argparse.ArgumentParser(description="ICT Engine v5.0 - Auto Start")
    parser.add_argument("--debug", action="store_true", help="Modo debug")
    parser.add_argument("--verbose", "-v", action="store_true", help="Output verbose")

    args = parser.parse_args()

    try:
        auto_start_dashboard(debug_mode=args.debug, verbose=args.verbose)
    except KeyboardInterrupt:
        enviar_senal_log("INFO", "\n❌ Operación cancelada por el usuario", "auto_start", "shutdown")
        sys.exit(0)
    except Exception as e:
        enviar_senal_log("ERROR", f"❌ Error crítico: {e}", "auto_start", "shutdown")
        sys.exit(1)

if __name__ == "__main__":
    main()
