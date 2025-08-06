"""
🔧 CORRECTOR DE INDENTACIÓN POST-MIGRACIÓN
==========================================

Corrige errores de indentación introducidos durante la migración al SIC.

Autor: Sistema Sentinel Grid
Fecha: 2025-08-06
Versión: v1.0
"""

import re
from pathlib import Path

def fix_indentation_in_file(file_path: Path) -> bool:
    """Corrige errores de indentación en un archivo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Detectar y corregir líneas con indentación incorrecta en imports
        lines = content.split('\n')
        fixed_lines = []

        for line in lines:
            # Si es una línea de import con indentación incorrecta
            if line.strip().startswith(('import ', 'from ')) and line.startswith('    '):
                # Remover indentación extra
                fixed_line = line.lstrip()
                fixed_lines.append(fixed_line)
                print(f"   ✅ Corregido: {line.strip()}")
            else:
                fixed_lines.append(line)

        # Escribir archivo corregido
        new_content = '\n'.join(fixed_lines)

        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True

        return False

    except Exception as e:
        print(f"❌ Error procesando {file_path}: {e}")
        return False

def main():
    """Función principal del corrector"""
    project_root = Path(__file__).parent.parent

    # Archivos migrados que necesitan corrección
    migrated_files = [
        "dashboard/dashboard_definitivo.py",
        "core/ict_engine/ict_detector.py",
        "dashboard/dashboard_widgets.py",
        "core/analysis_command_center/tct_pipeline/tct_interface.py",
        "core/analytics/ict_analyzer.py",
        "core/data_management/advanced_candle_downloader.py",
        "dashboard/hibernation_widget_v2.py",
        "dashboard/poi_dashboard_integration.py"
    ]

    print("🔧 CORRECTOR DE INDENTACIÓN POST-MIGRACIÓN")
    print("=" * 50)

    fixed_count = 0

    for file_rel_path in migrated_files:
        file_path = project_root / file_rel_path
        if file_path.exists():
            print(f"\n🎯 Procesando: {file_rel_path}")
            if fix_indentation_in_file(file_path):
                fixed_count += 1
                print(f"   ✅ Indentación corregida")
            else:
                print(f"   ✅ No requiere corrección")
        else:
            print(f"⚠️  Archivo no encontrado: {file_rel_path}")

    print(f"\n{'='*50}")
    print(f"📊 REPORTE FINAL")
    print(f"{'='*50}")
    print(f"✅ Archivos corregidos: {fixed_count}")
    print(f"🎉 Corrección de indentación completada")

if __name__ == "__main__":
    main()
