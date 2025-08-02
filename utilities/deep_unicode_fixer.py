# -*- coding: utf-8 -*-
# DEEP UNICODE FIXER - Sprint 1.1
# Reemplaza TODOS los emojis Unicode problemáticos

import os
import re
import sys
from pathlib import Path

def deep_fix_unicode():
    """
    Comprehensive fix for all Unicode emoji issues
    """
    project_root = Path(__file__).parent.parent

    # Archivos a arreglar
    files_to_fix = [
        project_root / "utilities" / "migration" / "print_migration_tool.py",
        project_root / "utilities" / "sprint" / "sprint_1_1_consolidator.py"
    ]

    files_fixed = 0

    for file_path in files_to_fix:
        if not file_path.exists():
            print(f"[WARNING] File not found: {file_path}")
            continue

        try:
            # Leer archivo
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Reemplazar secuencias Unicode \\U0001XXXX
            content = re.sub(r'\\U0001[0-9a-fA-F]{4}', '[EMOJI]', content)

            # Reemplazar f-strings que contengan \\U
            content = re.sub(r'f"[^"]*\\U[^"]*"', 'f"[FORMATTED_MSG]"', content)
            content = re.sub(r"f'[^']*\\U[^']*'", "f'[FORMATTED_MSG]'", content)

            # Limpiar prints problemáticos específicos
            problematic_prints = [
                r'print\(f"\\U[^"]*"\)',
                r"print\(f'\\U[^']*'\)",
                r'print\(f"[^"]*\\U[^"]*"[^)]*\)',
                r"print\(f'[^']*\\U[^']*'[^)]*\)"
            ]

            for pattern in problematic_prints:
                content = re.sub(pattern, 'print("[MSG]")', content)

            # Solo escribir si hay cambios
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"[OK] Deep fixed Unicode in: {file_path.name}")
                files_fixed += 1
            else:
                print(f"[OK] No Unicode issues in: {file_path.name}")

        except Exception as e:
            print(f"[ERROR] Error fixing {file_path}: {e}")

    print(f"\n[RESULT] Deep fixed Unicode in {files_fixed} files")

if __name__ == "__main__":
    print("[LAUNCH] Deep Unicode Fixer - Sprint 1.1")
    print("=" * 50)
    deep_fix_unicode()
