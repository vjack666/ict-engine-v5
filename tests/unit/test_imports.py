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
        enviar_senal_log("INFO", "✅ dashboard.dashboard_definitivo.SentinelDashboardDefinitivo - OK", "test_imports", "migration")
    except ImportError as e:
        missing_modules.append(f"❌ dashboard.dashboard_definitivo.SentinelDashboardDefinitivo - ERROR: {e}")
        enviar_senal_log("ERROR", f"❌ dashboard.dashboard_definitivo.SentinelDashboardDefinitivo - ERROR: {e}", "test_imports", "migration")

    # 🔧 Sistema imports
    try:
        from sistema.logging_interface import enviar_senal_log
        enviar_senal_log("INFO", "✅ sistema.logging_interface.enviar_senal_log - OK", "test_imports", "migration")
    except ImportError as e:
        missing_modules.append(f"❌ sistema.logging_interface.enviar_senal_log - ERROR: {e}")
        enviar_senal_log("ERROR", f"❌ sistema.logging_interface.enviar_senal_log - ERROR: {e}", "test_imports", "migration")

    # 🏗️ Core ICT imports
    try:
        from core.ict_engine.veredicto_engine_v4 import VeredictoEngine
        enviar_senal_log("INFO", "✅ core.ict_engine.veredicto_engine_v4.VeredictoEngine - OK", "test_imports", "migration")
    except ImportError as e:
        missing_modules.append(f"❌ core.ict_engine.veredicto_engine_v4.VeredictoEngine - ERROR: {e}")
        enviar_senal_log("ERROR", f"❌ core.ict_engine.veredicto_engine_v4.VeredictoEngine - ERROR: {e}", "test_imports", "migration")

    # 📊 Config imports
    try:
        from config.config_manager import ConfigManager
        enviar_senal_log("INFO", "✅ config.config_manager.ConfigManager - OK", "test_imports", "migration")
    except ImportError as e:
        missing_modules.append(f"❌ config.config_manager.ConfigManager - ERROR: {e}")
        enviar_senal_log("ERROR", f"❌ config.config_manager.ConfigManager - ERROR: {e}", "test_imports", "migration")

    # 📡 MT5 imports
    try:
        from utils.mt5_data_manager import MT5DataManager
        enviar_senal_log("INFO", "✅ utils.mt5_data_manager.MT5DataManager - OK", "test_imports", "migration")
    except ImportError as e:
        missing_modules.append(f"❌ utils.mt5_data_manager.MT5DataManager - ERROR: {e}")
        enviar_senal_log("ERROR", f"❌ utils.mt5_data_manager.MT5DataManager - ERROR: {e}", "test_imports", "migration")

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
            enviar_senal_log("INFO", f"✅ {dep} - OK", "test_imports", "migration")
        except ImportError as e:
            missing_deps.append(f"❌ {dep} - ERROR: {e}")
            enviar_senal_log("ERROR", f"❌ {dep} - ERROR: {e}", "test_imports", "migration")

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
            enviar_senal_log("INFO", f"✅ {file_path} - EXISTS", "test_imports", "migration")
        else:
            missing_files.append(f"❌ {file_path} - NOT FOUND")
            enviar_senal_log("INFO", f"❌ {file_path} - NOT FOUND", "test_imports", "migration")

    return missing_files

def main():
    """Función principal de diagnóstico"""
    enviar_senal_log("INFO", "🔍 DIAGNÓSTICO COMPLETO DE IMPORTS Y DEPENDENCIAS", "test_imports", "migration")
    enviar_senal_log("INFO", "=" * 60, "test_imports", "migration")

    enviar_senal_log("INFO", "\n📦 VERIFICANDO IMPORTS DEL CORE...", "test_imports", "migration")
    missing_modules = test_core_imports()

    enviar_senal_log("INFO", "\n🌐 VERIFICANDO DEPENDENCIAS EXTERNAS...", "test_imports", "migration")
    missing_deps = test_external_dependencies()

    enviar_senal_log("INFO", "\n📁 VERIFICANDO ESTRUCTURA DE ARCHIVOS...", "test_imports", "migration")
    missing_files = test_file_structure()

    enviar_senal_log("INFO", "\n" + "=" * 60, "test_imports", "migration")
    enviar_senal_log("INFO", "📋 RESUMEN DE PROBLEMAS ENCONTRADOS:", "test_imports", "migration")

    if missing_modules:
        enviar_senal_log("INFO", "\n❌ MÓDULOS FALTANTES:", "test_imports", "migration")
        for module in missing_modules:
            enviar_senal_log("INFO", f"  {module}", "test_imports", "migration")

    if missing_deps:
        enviar_senal_log("INFO", "\n❌ DEPENDENCIAS FALTANTES:", "test_imports", "migration")
        for dep in missing_deps:
            enviar_senal_log("INFO", f"  {dep}", "test_imports", "migration")

    if missing_files:
        enviar_senal_log("INFO", "\n❌ ARCHIVOS FALTANTES:", "test_imports", "migration")
        for file in missing_files:
            enviar_senal_log("INFO", f"  {file}", "test_imports", "migration")

    if not missing_modules and not missing_deps and not missing_files:
        enviar_senal_log("INFO", "\n✅ TODOS LOS IMPORTS Y DEPENDENCIAS ESTÁN OK", "test_imports", "migration")

    enviar_senal_log("INFO", "\n🎯 INFORMACIÓN PARA BITÁCORA:", "test_imports", "migration")
    enviar_senal_log("INFO", f"📁 Project Root: {project_root}", "test_imports", "migration")
    enviar_senal_log("INFO", f"🐍 Python: {sys.version}", "test_imports", "migration")
    enviar_senal_log("INFO", f"📂 Working Directory: {os.getcwd(, "test_imports", "migration")}")

if __name__ == "__main__":
    main()
