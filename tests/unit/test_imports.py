# 🔍 TEST DE IMPORTS - DIAGNÓSTICO COMPLETO
# Verificar qué módulos faltan para crear plan de trabajo

import sys
import os
from pathlib import Path

# Configurar path del proyecto
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def test_core_imports():
    """Test de imports del core del sistema"""
    missing_modules = []

    # 🎯 Dashboard imports
    try:
        from dashboard.dashboard_definitivo import SentinelDashboardDefinitivo as SentinelDashboard
        print("✅ dashboard.dashboard_definitivo.SentinelDashboardDefinitivo - OK")
    except ImportError as e:
        missing_modules.append(f"❌ dashboard.dashboard_definitivo.SentinelDashboardDefinitivo - ERROR: {e}")
        print(f"❌ dashboard.dashboard_definitivo.SentinelDashboardDefinitivo - ERROR: {e}")

    # 🔧 Sistema imports
    try:
        from sistema.logging_interface import enviar_senal_log
        print("✅ sistema.logging_interface.enviar_senal_log - OK")
    except ImportError as e:
        missing_modules.append(f"❌ sistema.logging_interface.enviar_senal_log - ERROR: {e}")
        print(f"❌ sistema.logging_interface.enviar_senal_log - ERROR: {e}")

    # 🏗️ Core ICT imports
    try:
        from core.ict_engine.veredicto_engine_v4 import VeredictoEngine
        print("✅ core.ict_engine.veredicto_engine_v4.VeredictoEngine - OK")
    except ImportError as e:
        missing_modules.append(f"❌ core.ict_engine.veredicto_engine_v4.VeredictoEngine - ERROR: {e}")
        print(f"❌ core.ict_engine.veredicto_engine_v4.VeredictoEngine - ERROR: {e}")

    # 📊 Config imports
    try:
        from config.config_manager import ConfigManager
        print("✅ config.config_manager.ConfigManager - OK")
    except ImportError as e:
        missing_modules.append(f"❌ config.config_manager.ConfigManager - ERROR: {e}")
        print(f"❌ config.config_manager.ConfigManager - ERROR: {e}")

    # 📡 MT5 imports
    try:
        from utils.mt5_data_manager import MT5DataManager
        print("✅ utils.mt5_data_manager.MT5DataManager - OK")
    except ImportError as e:
        missing_modules.append(f"❌ utils.mt5_data_manager.MT5DataManager - ERROR: {e}")
        print(f"❌ utils.mt5_data_manager.MT5DataManager - ERROR: {e}")

    return missing_modules

def test_external_dependencies():
    """Test de dependencias externas"""
    missing_deps = []

    dependencies = [
        'textual',
        'rich',
        'pandas',
        'numpy',
        'MetaTrader5',
        'pydantic',
        'dotenv'  # python-dotenv se importa como 'dotenv'
    ]

    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep} - OK")
        except ImportError as e:
            missing_deps.append(f"❌ {dep} - ERROR: {e}")
            print(f"❌ {dep} - ERROR: {e}")

    return missing_deps

def test_file_structure():
    """Test de estructura de archivos"""
    missing_files = []

    critical_files = [
        "dashboard/dashboard_definitivo.py",
        "sistema/logging_interface.py",
        "core/ict_engine/veredicto_engine_v4.py",
        "config/config_manager.py",
        "utils/mt5_data_manager.py",
        "main.py"
    ]

    for file_path in critical_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✅ {file_path} - EXISTS")
        else:
            missing_files.append(f"❌ {file_path} - NOT FOUND")
            print(f"❌ {file_path} - NOT FOUND")

    return missing_files

def main():
    """Función principal de diagnóstico"""
    print("🔍 DIAGNÓSTICO COMPLETO DE IMPORTS Y DEPENDENCIAS")
    print("=" * 60)

    print("\n📦 VERIFICANDO IMPORTS DEL CORE...")
    missing_modules = test_core_imports()

    print("\n🌐 VERIFICANDO DEPENDENCIAS EXTERNAS...")
    missing_deps = test_external_dependencies()

    print("\n📁 VERIFICANDO ESTRUCTURA DE ARCHIVOS...")
    missing_files = test_file_structure()

    print("\n" + "=" * 60)
    print("📋 RESUMEN DE PROBLEMAS ENCONTRADOS:")

    if missing_modules:
        print("\n❌ MÓDULOS FALTANTES:")
        for module in missing_modules:
            print(f"  {module}")

    if missing_deps:
        print("\n❌ DEPENDENCIAS FALTANTES:")
        for dep in missing_deps:
            print(f"  {dep}")

    if missing_files:
        print("\n❌ ARCHIVOS FALTANTES:")
        for file in missing_files:
            print(f"  {file}")

    if not missing_modules and not missing_deps and not missing_files:
        print("\n✅ TODOS LOS IMPORTS Y DEPENDENCIAS ESTÁN OK")

    print("\n🎯 INFORMACIÓN PARA BITÁCORA:")
    print(f"📁 Project Root: {project_root}")
    print(f"🐍 Python: {sys.version}")
    print(f"📂 Working Directory: {os.getcwd()}")

if __name__ == "__main__":
    main()
