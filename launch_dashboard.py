#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 LAUNCHER DASHBOARD POI INTEGRATION
====================================
Launcher optimizado para el dashboard con POI Integration
"""

import sys
import os

# Configurar path correcto
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

print("🚀 INICIANDO DASHBOARD CON POI INTEGRATION...")
print("=" * 50)

try:
    # Verificar imports críticos primero
    print("📦 Verificando imports críticos...")
    from sistema.logging_interface import enviar_senal_log
    from dashboard.poi_dashboard_integration import integrar_multi_poi_en_panel_ict
    print("✅ POI Integration disponible")

    # Importar y ejecutar el dashboard
    print("🎯 Lanzando Dashboard Definitivo...")
    import dashboard.dashboard_definitivo

except Exception as e:
    print(f"❌ Error al lanzar dashboard: {e}")
    import traceback
    print("Stack trace:")
    print(traceback.format_exc())
