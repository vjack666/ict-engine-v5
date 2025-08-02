#!/usr/bin/env python3
"""
🔧 CORRECTOR DE ENCODING DE LOGS
===============================
Convierte logs con encoding corrupto a UTF-8 correcto.
"""

import os
import sys
from pathlib import Path

def fix_log_encoding(log_file_path: str, backup=True):
    """
    Corrige el encoding de un archivo de log.

    Args:
        log_file_path: Ruta al archivo de log
        backup: Si crear backup del archivo original
    """
    log_path = Path(log_file_path)

    if not log_path.exists():
        print(f"❌ Archivo no encontrado: {log_file_path}")
        return False

    print(f"🔧 Corrigiendo encoding de: {log_file_path}")

    # Crear backup si se solicita
    if backup:
        backup_path = log_path.with_suffix(log_path.suffix + '.backup')
        log_path.rename(backup_path)
        print(f"📁 Backup creado: {backup_path}")

    try:
        # Leer con encoding corrupto
        with open(backup_path if backup else log_path, 'r', encoding='latin-1') as f:
            content = f.read()

        # Escribir con UTF-8 correcto
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Encoding corregido exitosamente")
        return True

    except Exception as e:
        print(f"❌ Error corrigiendo encoding: {e}")
        return False

def main():
    print("🔧 CORRECTOR DE ENCODING DE LOGS")
    print("=" * 40)

    # Archivos de log a corregir
    log_files = [
        "data/logs/trading/trading_decisions.log",
        "data/logs/errors/error.log",
        "data/logs/mt5/mt5_operations.log"
    ]

    for log_file in log_files:
        if Path(log_file).exists():
            fix_log_encoding(log_file)
        else:
            print(f"⚠️ Archivo no encontrado: {log_file}")

    print()
    print("✅ Corrección de encoding completada")

if __name__ == "__main__":
    main()
