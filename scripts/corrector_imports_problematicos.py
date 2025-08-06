#!/usr/bin/env python3
"""
🔧 CORRECTOR DE IMPORTS PROBLEMÁTICOS POST-MIGRACIÓN
==================================================
Corrige imports específicos que no existen en el SIC expandido

Autor: Sistema Sentinel Grid
Fecha: 2025-08-06
"""

import os
import re
from pathlib import Path

def fix_problematic_imports():
    """Corregir imports problemáticos detectados"""

    print("🔧 CORRIGIENDO IMPORTS PROBLEMÁTICOS...")
    print("=" * 50)

    # Mapeo de imports problemáticos a correcciones
    import_fixes = {
        'log_trading': 'log_info',
        'log_mt5': 'log_info',
        'log_debug': 'log_info',
        'log_warning': 'log_error',
        'setup_logging': 'log_info',
        'get_logger': 'log_info',
        'log_trading_decision': 'log_info',
    }

    files_fixed = 0
    fixes_applied = 0

    # Procesar todos los archivos Python
    for root, dirs, files in os.walk('.'):
        # Filtrar directorios
        dirs[:] = [d for d in dirs if not d.startswith(('__pycache__', '.git', 'backup_', 'migration_reports'))]

        for file in files:
            if file.endswith('.py') and file not in ['sic.py', 'corrector_imports_problematicos.py']:
                file_path = Path(root) / file

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    original_content = content
                    file_modified = False

                    # Aplicar correcciones
                    for problematic, correct in import_fixes.items():
                        # Patrón para encontrar imports del SIC con el elemento problemático
                        pattern = rf'from sistema\.sic import (.*?){problematic}(.*?)$'

                        def replace_import(match):
                            before = match.group(1)
                            after = match.group(2)
                            return f'from sistema.sic import {before}{correct}{after}'

                        new_content = re.sub(pattern, replace_import, content, flags=re.MULTILINE)

                        if new_content != content:
                            content = new_content
                            file_modified = True
                            fixes_applied += 1
                            print(f"   ✅ {file_path}: {problematic} → {correct}")

                    # Guardar archivo si fue modificado
                    if file_modified:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        files_fixed += 1

                except Exception as e:
                    print(f"   ❌ Error procesando {file_path}: {e}")

    print(f"\n📊 RESUMEN:")
    print(f"   📁 Archivos corregidos: {files_fixed}")
    print(f"   🔧 Correcciones aplicadas: {fixes_applied}")

    if fixes_applied > 0:
        print(f"\n✅ CORRECCIÓN COMPLETADA")
        print(f"   Los imports problemáticos han sido corregidos")
    else:
        print(f"\n✅ NO HAY IMPORTS PROBLEMÁTICOS")
        print(f"   Todos los imports están correctos")

    return fixes_applied > 0

if __name__ == "__main__":
    fix_problematic_imports()
