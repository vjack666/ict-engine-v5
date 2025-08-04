#!/usr/bin/env python3
"""
🎯 ICT ENGINE v5.0 - DASHBOARD DIRECTO
=====================================

Launcher simplificado que va directo al dashboard principal
sin auto-descarga ni menús adicionales.

Uso:
    python dashboard_directo.py
"""

import sys
import os
from pathlib import Path

# 📁 Configurar paths del proyecto
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from sistema.logging_interface import enviar_senal_log

def main():
    """Lanza directamente el dashboard"""

    print("🎯 ICT ENGINE v5.0 - DASHBOARD DIRECTO")
    print("=====================================")
    print("📊 Usando datos REALES de MT5")
    print("🚀 Iniciando dashboard...")
    print()

    try:
        from dashboard.dashboard_definitivo import SentinelDashboardDefinitivo

        # 🎯 INICIAR DASHBOARD DIRECTAMENTE
        app = SentinelDashboardDefinitivo()
        app.run()

    except ImportError as e:
        print(f"❌ Error importando dashboard: {e}")
        print("🔧 Asegúrate de que todos los módulos estén instalados")
        input("Presiona Enter para continuar...")
        return False
    except KeyboardInterrupt:
        print("\n👋 ¡Dashboard cerrado!")
        return True
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        input("Presiona Enter para continuar...")
        return False

    return True

if __name__ == "__main__":
    main()
