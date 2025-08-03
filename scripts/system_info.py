from sistema.logging_interface import enviar_senal_log
#!/usr/bin/env python3
"""
📊 System Information Tool
========================

Herramienta para mostrar información detallada del sistema ICT Engine.
"""

import sys
import os
import platform
from pathlib import Path
from datetime import datetime

def main():
    """Función principal"""
    enviar_senal_log("INFO", "📊 ICT ENGINE v5.0 - INFORMACIÓN DEL SISTEMA", "system_info", "migration")
    enviar_senal_log("INFO", "=" * 60, "system_info", "migration")

    # 🖥️ Información del sistema
    enviar_senal_log("INFO", f"\n🖥️ SISTEMA OPERATIVO:", "system_info", "migration")
    enviar_senal_log("INFO", f"  Sistema: {platform.system(, "system_info", "migration")}")
    enviar_senal_log("INFO", f"  Versión: {platform.version(, "system_info", "migration")}")
    enviar_senal_log("INFO", f"  Arquitectura: {platform.architecture(, "system_info", "migration")[0]}")
    enviar_senal_log("INFO", f"  Procesador: {platform.processor(, "system_info", "migration")}")

    # 🐍 Información de Python
    enviar_senal_log("INFO", f"\n🐍 PYTHON:", "system_info", "migration")
    enviar_senal_log("INFO", f"  Versión: {sys.version}", "system_info", "migration")
    enviar_senal_log("INFO", f"  Ejecutable: {sys.executable}", "system_info", "migration")
    enviar_senal_log("INFO", f"  Path: {':'.join(sys.path[:3], "system_info", "migration")}...")

    # 📁 Información del proyecto
    project_root = Path(__file__).parent.parent
    enviar_senal_log("INFO", f"\n📁 PROYECTO:", "system_info", "migration")
    enviar_senal_log("INFO", f"  Directorio: {project_root}", "system_info", "migration")
    enviar_senal_log("INFO", f"  Tamaño: {get_directory_size(project_root, "system_info", "migration"):.2f} MB")
    enviar_senal_log("INFO", f"  Archivos Python: {count_python_files(project_root, "system_info", "migration")}")

    # ⏰ Información temporal
    enviar_senal_log("INFO", f"\n⏰ TIEMPO:", "system_info", "migration")
    enviar_senal_log("INFO", f"  Fecha actual: {datetime.now(, "system_info", "migration").strftime('%Y-%m-%d %H:%M:%S')}")
    enviar_senal_log("INFO", f"  Zona horaria: {datetime.now(, "system_info", "migration").astimezone().tzinfo}")

def get_directory_size(path: Path) -> float:
    """Calcula el tamaño de un directorio en MB"""
    total_size = 0
    try:
        for file_path in path.rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
    except:
        pass
    return total_size / (1024 * 1024)

def count_python_files(path: Path) -> int:
    """Cuenta archivos Python en el directorio"""
    try:
        return len(list(path.rglob("*.py")))
    except:
        return 0

if __name__ == "__main__":
    main()
