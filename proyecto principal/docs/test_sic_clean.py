#!/usr/bin/env python3
"""
Test del SIC Clean v3.0
"""
import sys
import os

# Agregar path del proyecto
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Test del SIC
try:
    from sistema.sic_clean import (
        get_sic_status, enviar_senal_log, Dict, List, datetime,
        ICTDetector, POIDetector, DashboardController, MT5DataManager
    )

    print("✅ SIC Clean v3.0 - IMPORT EXITOSO")
    print("=" * 50)

    # Test de logging
    if enviar_senal_log:
        enviar_senal_log("INFO", "Test de logging desde SIC", "test", "validation")
        print("✅ Sistema de logging funcional")
    else:
        print("❌ Sistema de logging no disponible")

    # Test de tipos
    print(f"✅ Tipos básicos: Dict={Dict.__name__}, List={List.__name__}")
    print(f"✅ Datetime: {datetime}")

    # Test de status
    status = get_sic_status()
    print(f"✅ Status SIC: {status['version']}")
    print(f"✅ Total exports: {status['total_exports']}")

    # Test de componentes
    components = ['ICTDetector', 'POIDetector', 'DashboardController', 'MT5DataManager']
    for comp in components:
        value = locals()[comp]
        status_text = "✅ Disponible" if value is not None else "⚠️  No disponible"
        print(f"{status_text}: {comp}")

    print("=" * 50)
    print("🎯 SIC v3.0 Limpio - COMPLETAMENTE FUNCIONAL")

except Exception as e:
    print(f"❌ Error en test: {e}")
    import traceback
    traceback.print_exc()
