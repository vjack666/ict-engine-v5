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

    print("🧪 INICIANDO TESTS DEL PANEL POI...")

    # Test 1: DataFrame None (caso más común)
    print("\n📊 Test 1: DataFrame None")
    panel_none = construir_panel_poi_multi(None, 1.1000, 'EURUSD')
    console.print(panel_none)

    # Test 2: DataFrame vacío
    print("\n📊 Test 2: DataFrame vacío")
    df_empty = pd.DataFrame()
    panel_empty = construir_panel_poi_multi(df_empty, 1.1000, 'EURUSD')
    console.print(panel_empty)

    # Test 3: DataFrame válido pequeño
    print("\n📊 Test 3: DataFrame pequeño (< 20 velas)")
    df_small = pd.DataFrame({
        'high': [1.1000, 1.1010],
        'low': [1.0990, 1.0995],
        'close': [1.0995, 1.1005]
    })
    panel_small = construir_panel_poi_multi(df_small, 1.1000, 'EURUSD')
    console.print(panel_small)

    print("\n✅ TODOS LOS TESTS COMPLETADOS SIN ERRORES")

except Exception as e:
    print(f"❌ ERROR EN TESTS: {e}")
    import traceback
    traceback.print_exc()
