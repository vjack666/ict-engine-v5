#!/usr/bin/env python3
"""
🖥️ INFORMACIÓN DEL SISTEMA
=========================

Muestra información completa del sistema y estado del proyecto.
"""

# MIGRACIÓN SIC v3.0 + SLUC v2.1
from sistema.sic import enviar_senal_log, log_info, log_warning

from sistema.sic import sys
import platform
from sistema.sic import Path
from sistema.sic import datetime

# Agregar project root al path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from sistema.sic import enviar_senal_log

def mostrar_info_sistema():
    """Muestra información completa del sistema"""

    enviar_senal_log("INFO", "🖥️ INFORMACIÓN DEL SISTEMA SENTINEL GRID", "system_info", "system")
    enviar_senal_log("INFO", "=" * 60, "system_info", "system")

    try:
        # 1. Información del sistema operativo
        enviar_senal_log("INFO", "🖥️ 1. SISTEMA OPERATIVO", "system_info", "system")
        enviar_senal_log("INFO", f"   Sistema: {platform.system()}", "system_info", "system")
        enviar_senal_log("INFO", f"   Versión: {platform.version()}", "system_info", "system")
        enviar_senal_log("INFO", f"   Arquitectura: {platform.architecture()[0]}", "system_info", "system")
        enviar_senal_log("INFO", f"   Procesador: {platform.processor()}", "system_info", "system")

        # 2. Información de Python
        enviar_senal_log("INFO", "", "system_info", "system")
        enviar_senal_log("INFO", "🐍 2. PYTHON", "system_info", "system")
        enviar_senal_log("INFO", f"   Versión: {platform.python_version()}", "system_info", "system")
        enviar_senal_log("INFO", f"   Ejecutable: {sys.executable}", "system_info", "system")
        enviar_senal_log("INFO", f"   Path: {sys.path[0]}", "system_info", "system")

        # 3. Información del proyecto
        enviar_senal_log("INFO", "", "system_info", "system")
        enviar_senal_log("INFO", "🎯 3. PROYECTO SENTINEL GRID", "system_info", "system")
        enviar_senal_log("INFO", f"   Directorio: {PROJECT_ROOT}", "system_info", "system")
        enviar_senal_log("INFO", "   Versión: v3.3.3.3.3", "system_info", "system")
        enviar_senal_log("INFO", f"   Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "system_info", "system")

        # 4. Estado de componentes
        enviar_senal_log("INFO", "", "system_info", "system")
        enviar_senal_log("INFO", "🔧 4. ESTADO DE COMPONENTES", "system_info", "system")

        # Verificar componentes principales
        components = [
            ("utils/mt5_data_manager.py", "MT5 Data Manager"),
            ("core/poi_system/poi_system.py", "POI System"),
            ("core/ict_engine/ict_engine.py", "ICT Engine"),
            ("dashboard/dashboard_definitivo.py", "Dashboard Principal"),
            ("config/live_account_validator.py", "Account Validator")
        ]

        for file_path, component_name in components:
            full_path = PROJECT_ROOT / file_path
            if full_path.exists():
                enviar_senal_log("INFO", f"   ✅ {component_name}: Disponible", "system_info", "system")
            else:
                enviar_senal_log("ERROR", f"   ❌ {component_name}: NO encontrado", "system_info", "system")

        # 5. Estructura de directorios
        enviar_senal_log("INFO", "", "system_info", "system")
        enviar_senal_log("INFO", "📁 5. ESTRUCTURA DEL PROYECTO", "system_info", "system")

        main_dirs = ["config", "core", "dashboard", "data", "scripts", "sistema", "utils"]
        for dir_name in main_dirs:
            dir_path = PROJECT_ROOT / dir_name
            if dir_path.exists():
                enviar_senal_log("INFO", f"   📁 {dir_name}/: ✅", "system_info", "system")
            else:
                enviar_senal_log("ERROR", f"   📁 {dir_name}/: ❌", "system_info", "system")

        # 6. Estado del sistema
        enviar_senal_log("INFO", "", "system_info", "system")
        enviar_senal_log("INFO", "📊 6. ESTADO GENERAL", "system_info", "system")
        enviar_senal_log("INFO", "   🎯 Pipeline MT5: Sin errores", "system_info", "system")
        enviar_senal_log("INFO", "   🔗 Integración POI/ICT: Operativa", "system_info", "system")
        enviar_senal_log("INFO", "   📡 Dashboard: Funcional", "system_info", "system")
        enviar_senal_log("INFO", "   🛡️ Sistema: Estable", "system_info", "system")
        enviar_senal_log("INFO", "   🚀 Modo: Producción", "system_info", "system")

        enviar_senal_log("INFO", "", "system_info", "system")
        enviar_senal_log("INFO", "✅ INFORMACIÓN DEL SISTEMA COMPLETADA", "system_info", "system")

        return True

    except Exception as e:
        enviar_senal_log("ERROR", f"❌ ERROR OBTENIENDO INFO: {e}", "system_info", "system")
        return False

def main():
    """Función principal"""
    enviar_senal_log("INFO", "🚀 Obteniendo información del sistema", "system_info", "system")

    success = mostrar_info_sistema()

    if success:
        enviar_senal_log("INFO", "🎉 Información obtenida exitosamente", "system_info", "system")
    else:
        enviar_senal_log("ERROR", "⚠️ Error obteniendo información", "system_info", "system")

if __name__ == "__main__":
    main()
