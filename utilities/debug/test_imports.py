#!/usr/bin/env python3
"""
🔍 TEST DE IMPORTS - Diagnóstico de importaciones
================================================

Script para verificar que todos los imports críticos funcionen correctamente.
"""

import sys
import os

# Agregar path raíz del proyecto
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

def test_core_imports():
    """Probar todos los imports del core ICT Engine"""
    print("🧪 Testing core ICT Engine imports...")

    try:
        from core.ict_engine import ict_types
        print("✅ ict_types imported successfully")
    except Exception as e:
        print(f"❌ ict_types failed: {e}")

    try:
        from core.ict_engine import ict_detector
        print("✅ ict_detector imported successfully")
    except Exception as e:
        print(f"❌ ict_detector failed: {e}")

    try:
        from core.ict_engine import pattern_analyzer
        print("✅ pattern_analyzer imported successfully")
    except Exception as e:
        print(f"❌ pattern_analyzer failed: {e}")

    try:
        from core.ict_engine import confidence_engine
        print("✅ confidence_engine imported successfully")
    except Exception as e:
        print(f"❌ confidence_engine failed: {e}")

    try:
        from core.ict_engine import veredicto_engine_v4
        print("✅ veredicto_engine_v4 imported successfully")
    except Exception as e:
        print(f"❌ veredicto_engine_v4 failed: {e}")

    try:
        from core.ict_engine import ict_historical_analyzer
        print("✅ ict_historical_analyzer imported successfully")
    except Exception as e:
        print(f"❌ ict_historical_analyzer failed: {e}")

def test_dashboard_imports():
    """Probar imports del dashboard"""
    print("\n🖥️ Testing dashboard imports...")

    try:
        from dashboard import dashboard_definitivo
        print("✅ dashboard_definitivo imported successfully")
    except Exception as e:
        print(f"❌ dashboard_definitivo failed: {e}")

def test_system_imports():
    """Probar imports del sistema"""
    print("\n🔧 Testing system imports...")

    try:
        from sistema import logging_config
        print("✅ logging_config imported successfully")
    except Exception as e:
        print(f"❌ logging_config failed: {e}")

    try:
        from config import config_manager
        print("✅ config_manager imported successfully")
    except Exception as e:
        print(f"❌ config_manager failed: {e}")

if __name__ == "__main__":
    print("🔍 DIAGNÓSTICO DE IMPORTS")
    print("=" * 50)
    print(f"📁 Project root: {project_root}")
    print(f"🐍 Python path: {sys.path[:3]}")
    print()

    test_core_imports()
    test_dashboard_imports()
    test_system_imports()

    print("\n✅ Diagnóstico completado")
