# -*- coding: utf-8 -*-
# WINDOWS EMOJI FIXER - Sprint 1.1
# Reemplaza emojis Unicode problemáticos con versiones Windows-compatible

import os
import re
import sys
from pathlib import Path

def fix_unicode_issues():
    """
    Fix emoji encoding issues in Sprint 1.1 files for Windows compatibility
    """
    project_root = Path(__file__).parent.parent

    # Archivos a arreglar
    files_to_fix = [
        project_root / "utilities" / "migration" / "print_migration_tool.py",
        project_root / "utilities" / "sprint" / "sprint_1_1_consolidator.py"
    ]

    # Mapeo de emojis problemáticos a versiones seguras
    emoji_fixes = {
        "🔍": "[SCAN]",
        "🎯": "[TARGET]",
        "🔧": "[TOOL]",
        "✅": "[OK]",
        "❌": "[ERROR]",
        "⚠️": "[WARNING]",
        "🚀": "[LAUNCH]",
        "📊": "[REPORT]",
        "📁": "[FOLDER]",
        "🎉": "[SUCCESS]",
        "🔢": "[NUMBER]",
        "🎪": "[RESULT]",
        "💾": "[SAVE]",
        "📝": "[LOG]",
        "🏃‍♂️": "[RUN]",
        "🏃": "[RUN]"
    }

    files_fixed = 0

    for file_path in files_to_fix:
        if not file_path.exists():
            print(f"[WARNING] File not found: {file_path}")
            continue

        try:
            # Leer archivo
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Aplicar fixes
            original_content = content
            for emoji, replacement in emoji_fixes.items():
                content = content.replace(emoji, replacement)

            # Solo escribir si hay cambios
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"[OK] Fixed emojis in: {file_path.name}")
                files_fixed += 1
            else:
                print(f"[OK] No emojis to fix in: {file_path.name}")

        except Exception as e:
            print(f"[ERROR] Error fixing {file_path}: {e}")

    print(f"\n[RESULT] Fixed emojis in {files_fixed} files")
    print("[OK] Sprint 1.1 should now work on Windows!")

if __name__ == "__main__":
    print("[LAUNCH] Windows Emoji Fixer - Sprint 1.1")
    print("=" * 50)
    fix_unicode_issues()
