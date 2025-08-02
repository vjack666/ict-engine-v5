# -*- coding: utf-8 -*-
# FINAL EMOJI CLEANUP - Sprint 1.1

import re
from pathlib import Path

def final_cleanup():
    """
    Cleanup final de todos los emojis problemáticos
    """
    project_root = Path(__file__).parent.parent

    files_to_clean = [
        project_root / "utilities" / "migration" / "print_migration_tool.py",
        project_root / "utilities" / "sprint" / "sprint_1_1_consolidator.py"
    ]

    # Reemplazos exhaustivos
    replacements = {
        "📈": "[CHART]",
        "🧪": "[TEST]",
        "⏳": "[PENDING]",
        "📋": "[LIST]",
        "📄": "[FILE]",
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

    for file_path in files_to_clean:
        if not file_path.exists():
            continue

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original = content

            # Aplicar reemplazos
            for emoji, replacement in replacements.items():
                content = content.replace(emoji, replacement)

            # Regex para capturar emojis escapados Unicode
            content = re.sub(r'\\[uU][0-9a-fA-F]{4,8}', '[EMOJI]', content)

            if content != original:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"[OK] Cleaned: {file_path.name}")
            else:
                print(f"[OK] Clean: {file_path.name}")

        except Exception as e:
            print(f"[ERROR] {file_path}: {e}")

    print("[SUCCESS] Final cleanup completed!")

if __name__ == "__main__":
    final_cleanup()
