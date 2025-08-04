#!/usr/bin/env python3
"""
Script de prueba para ICTEngine - Diagnóstico completo
"""

import sys
import os
import traceback

# Añadir ruta del proyecto
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_basic_imports():
    """Test importaciones básicas"""
    print("=== TEST IMPORTACIONES BÁSICAS ===")

    try:
        import pandas as pd
        print("✅ pandas OK")
    except Exception as e:
        print(f"❌ pandas error: {e}")

    try:
        from datetime import datetime
        print("✅ datetime OK")
    except Exception as e:
        print(f"❌ datetime error: {e}")

    try:
        from sistema.logging_interface import enviar_senal_log
        print("✅ logging_interface OK")
    except Exception as e:
        print(f"❌ logging_interface error: {e}")

def test_ict_components():
    """Test componentes ICT individuales"""
    print("\n=== TEST COMPONENTES ICT ===")

    # Test ict_types
    try:
        from core.ict_engine.ict_types import ICTPattern
        print("✅ ict_types OK")
    except Exception as e:
        print(f"❌ ict_types error: {e}")
        traceback.print_exc()

    # Test ict_detector
    try:
        from core.ict_engine.ict_detector import ICTDetector
        print("✅ ict_detector OK")
    except Exception as e:
        print(f"❌ ict_detector error: {e}")
        traceback.print_exc()

    # Test confidence_engine
    try:
        from core.ict_engine.confidence_engine import ConfidenceEngine
        print("✅ confidence_engine OK")
    except Exception as e:
        print(f"❌ confidence_engine error: {e}")
        traceback.print_exc()

def test_ict_engine():
    """Test ICTEngine principal"""
    print("\n=== TEST ICT ENGINE PRINCIPAL ===")

    try:
        from core.ict_engine.ict_engine import ICTEngine, get_ict_engine
        print("✅ ICTEngine import OK")

        # Test instanciación
        engine = ICTEngine()
        print("✅ ICTEngine instanciación OK")

        # Test singleton
        engine1 = get_ict_engine()
        engine2 = get_ict_engine()
        print(f"✅ Singleton test: {engine1 is engine2}")

        return True

    except Exception as e:
        print(f"❌ ICTEngine error: {e}")
        traceback.print_exc()
        return False

def main():
    """Función principal de pruebas"""
    print("INICIANDO DIAGNÓSTICO ICT ENGINE")
    print("=" * 50)

    test_basic_imports()
    test_ict_components()
    success = test_ict_engine()

    print("\n" + "=" * 50)
    if success:
        print("✅ DIAGNÓSTICO COMPLETADO - ICT ENGINE FUNCIONA")
    else:
        print("❌ DIAGNÓSTICO COMPLETADO - PROBLEMAS DETECTADOS")

    return success

if __name__ == "__main__":
    main()
