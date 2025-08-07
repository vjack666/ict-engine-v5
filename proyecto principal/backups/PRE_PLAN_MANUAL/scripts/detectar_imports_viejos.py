#!/usr/bin/env python3
"""
🔍 DETECTAR ARCHIVOS CON IMPORTS VIEJOS
======================================
Encuentra archivos que no fueron procesados en Fase 3

Autor: Sistema Sentinel Grid
Fecha: 2025-08-06
"""

# MIGRACIÓN SIC v3.0 + SLUC v2.1
from sistema.sic import enviar_senal_log, log_info, log_warning

from sistema.sic import os
from sistema.sic import Path

def find_files_with_old_imports():
    """Encontrar archivos con imports viejos"""

    print("🔍 BUSCANDO ARCHIVOS CON IMPORTS VIEJOS...")
    print("=" * 50)

    old_patterns = [
        'from typing import',
        'from datetime import',
        'import os',
        'import sys',
        'import json',
        'from dataclasses import'
    ]

    problem_files = []

    for root, dirs, files in os.walk('.'):
        # Filtrar directorios
        dirs[:] = [d for d in dirs if not d.startswith(('__pycache__', '.git', 'backup_', 'migration_reports'))]

        for file in files:
            if file.endswith('.py') and file not in ['py', 'fase1_scan_imports.py', 'fase2_expandir_py', 'fase3_eliminar_imports.py', 'validador_final_estrategia.py', 'detectar_imports_viejos.py']:
                file_path = Path(root) / file

                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    # Si NO tiene import del SIC pero SÍ tiene imports viejos
                    if 'from sistema.sic import' not in content:
                        has_old_imports = []
                        for pattern in old_patterns:
                            if pattern in content:
                                has_old_imports.append(pattern)

                        if has_old_imports:
                            problem_files.append({
                                'file': str(file_path),
                                'old_imports': has_old_imports
                            })

                except Exception as e:
                    print(f"   ⚠️ Error leyendo {file_path}: {e}")

    if problem_files:
        print(f"📊 ARCHIVOS CON IMPORTS VIEJOS: {len(problem_files)}")
        print("")

        for item in problem_files:
            print(f"📄 {item['file']}")
            for imp in item['old_imports']:
                print(f"   🔴 {imp}")
            print("")
    else:
        print("✅ No se encontraron archivos con imports viejos")

    return problem_files

if __name__ == "__main__":
    find_files_with_old_imports()
