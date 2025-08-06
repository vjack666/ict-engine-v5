#!/usr/bin/env python3
"""
🧹 DETECTOR RÁPIDO DE LOGS OBSOLETOS
==================================

Versión simplificada para detectar logging obsoleto
"""

import re
from pathlib import Path

def scan_file_for_logging(file_path):
    """Escanea un archivo buscando referencias de logging"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        patterns = [
            (r'import\s+logging', 'import logging'),
            (r'from\s+logging\s+import', 'from logging import'),
            (r'logging\.getLogger', 'logging.getLogger'),
            (r'logger\.debug\s*\(', 'logger.debug()'),
            (r'logger\.info\s*\(', 'logger.info()'),
            (r'logger\.warning\s*\(', 'logger.warning()'),
            (r'logger\.error\s*\(', 'logger.error()'),
            (r'logging\.debug\s*\(', 'logging.debug()'),
            (r'logging\.info\s*\(', 'logging.info()'),
        ]

        issues = []
        lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            for pattern, description in patterns:
                if re.search(pattern, line) and not line.strip().startswith('#'):
                    issues.append({
                        'line': line_num,
                        'text': line.strip(),
                        'type': description
                    })

        return issues

    except Exception as e:
        print(f"Error procesando {file_path}: {e}")
        return []

def main():
    """Función principal"""
    PROJECT_ROOT = Path(__file__).parent

    print("🔍 DETECTANDO LOGS OBSOLETOS EN EL PROYECTO")
    print("=" * 50)

    # Directorios a escanear
    scan_dirs = [
        PROJECT_ROOT / "core",
        PROJECT_ROOT / "dashboard",
        PROJECT_ROOT / "scripts",
        PROJECT_ROOT / "sistema",
        PROJECT_ROOT / "utilities",
        PROJECT_ROOT / "config",
        PROJECT_ROOT,  # Archivos raíz
    ]

    total_files = 0
    files_with_issues = 0
    total_issues = 0

    for scan_dir in scan_dirs:
        if not scan_dir.exists():
            continue

        py_files = list(scan_dir.rglob("*.py"))

        for py_file in py_files:
            total_files += 1
            issues = scan_file_for_logging(py_file)

            if issues:
                files_with_issues += 1
                total_issues += len(issues)

                relative_path = py_file.relative_to(PROJECT_ROOT)
                print(f"\n📁 {relative_path} ({len(issues)} issues)")

                for issue in issues:
                    print(f"   🔸 Línea {issue['line']}: {issue['type']}")
                    print(f"      {issue['text'][:80]}...")

    print(f"\n📊 RESUMEN:")
    print(f"   📄 Archivos escaneados: {total_files}")
    print(f"   ⚠️ Archivos con problemas: {files_with_issues}")
    print(f"   🔥 Total issues: {total_issues}")

    if total_issues > 0:
        print(f"\n💡 ARCHIVOS QUE NECESITAN LIMPIEZA:")
        print("   - Reemplazar logger.* con enviar_senal_log")
        print("   - Eliminar imports de logging obsoletos")
        print("   - Verificar que ya existe import de enviar_senal_log")
    else:
        print("\n✅ No se encontraron logs obsoletos")

if __name__ == "__main__":
    main()
