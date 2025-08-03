# -*- coding: utf-8 -*-
# FINAL EMOJI CLEANUP - Sprint 1.1

import re
from pathlib import Path
from sistema.logging_interface import enviar_senal_log

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
                enviar_senal_log("INFO", f"[OK] Cleaned: {file_path.name}", "final_emoji_cleanup", "migration")
            else:
                enviar_senal_log("INFO", f"[OK] Clean: {file_path.name}", "final_emoji_cleanup", "migration")

        except Exception as e:
            enviar_senal_log("ERROR", f"[ERROR] {file_path}: {e}", "final_emoji_cleanup", "migration")

    enviar_senal_log("INFO", "[SUCCESS] Final cleanup completed!", "final_emoji_cleanup", "migration")

if __name__ == "__main__":
    final_cleanup()
