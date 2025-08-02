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
    print("📊 ICT ENGINE v5.0 - INFORMACIÓN DEL SISTEMA")
    print("=" * 60)

    # 🖥️ Información del sistema
    print(f"\n🖥️ SISTEMA OPERATIVO:")
    print(f"  Sistema: {platform.system()}")
    print(f"  Versión: {platform.version()}")
    print(f"  Arquitectura: {platform.architecture()[0]}")
    print(f"  Procesador: {platform.processor()}")

    # 🐍 Información de Python
    print(f"\n🐍 PYTHON:")
    print(f"  Versión: {sys.version}")
    print(f"  Ejecutable: {sys.executable}")
    print(f"  Path: {':'.join(sys.path[:3])}...")

    # 📁 Información del proyecto
    project_root = Path(__file__).parent.parent
    print(f"\n📁 PROYECTO:")
    print(f"  Directorio: {project_root}")
    print(f"  Tamaño: {get_directory_size(project_root):.2f} MB")
    print(f"  Archivos Python: {count_python_files(project_root)}")

    # ⏰ Información temporal
    print(f"\n⏰ TIEMPO:")
    print(f"  Fecha actual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Zona horaria: {datetime.now().astimezone().tzinfo}")

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
