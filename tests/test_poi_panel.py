from sistema.logging_interface import enviar_senal_log
"""
Test rápido para verificar el panel POI con manejo robusto de errores
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from dashboard.poi_dashboard_integration import construir_panel_poi_multi
    from rich.console import Console
    import pandas as pd

    console = Console()

    enviar_senal_log("INFO", "🧪 INICIANDO TESTS DEL PANEL POI...", "test_poi_panel", "migration")

    # Test 1: DataFrame None (caso más común)
    enviar_senal_log("INFO", "\n📊 Test 1: DataFrame None", "test_poi_panel", "migration")
    panel_none = construir_panel_poi_multi(None, 1.1000, 'EURUSD')
    console.enviar_senal_log("INFO", panel_none, "test_poi_panel", "migration")

    # Test 2: DataFrame vacío
    enviar_senal_log("INFO", "\n📊 Test 2: DataFrame vacío", "test_poi_panel", "migration")
    df_empty = pd.DataFrame()
    panel_empty = construir_panel_poi_multi(df_empty, 1.1000, 'EURUSD')
    console.enviar_senal_log("INFO", panel_empty, "test_poi_panel", "migration")

    # Test 3: DataFrame válido pequeño
    enviar_senal_log("INFO", "\n📊 Test 3: DataFrame pequeño (< 20 velas, "test_poi_panel", "migration")")
    df_small = pd.DataFrame({
        'high': [1.1000, 1.1010],
        'low': [1.0990, 1.0995],
        'close': [1.0995, 1.1005]
    })
    panel_small = construir_panel_poi_multi(df_small, 1.1000, 'EURUSD')
    console.enviar_senal_log("INFO", panel_small, "test_poi_panel", "migration")

    enviar_senal_log("ERROR", "\n✅ TODOS LOS TESTS COMPLETADOS SIN ERRORES", "test_poi_panel", "migration")

except Exception as e:
    enviar_senal_log("ERROR", f"❌ ERROR EN TESTS: {e}", "test_poi_panel", "migration")
    import traceback
    traceback.print_exc()
