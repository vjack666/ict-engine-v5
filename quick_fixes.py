#!/usr/bin/env python3
"""
🔧 QUICK FIXES AUTOMATION SCRIPT
===============================
Resuelve automáticamente los errores más comunes de Pylance.

Uso:
    python quick_fixes.py --scan      # Solo escanear
    python quick_fixes.py --fix       # Aplicar fixes
    python quick_fixes.py --all       # Escanear y aplicar
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple
import argparse

class QuickFixer:
    """Automatiza la corrección de errores comunes de Pylance."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.fixes_applied = {
            'unused_imports': 0,
            'unused_variables': 0,
            'json_decode_error': 0,
            'constant_redefinition': 0,
            'duplicate_imports': 0
        }

    def scan_and_fix_all(self, apply_fixes: bool = False) -> Dict:
        """Escanea y opcionalmente aplica todos los fixes."""
        print("🔍 ESCANEANDO PROYECTO PARA QUICK FIXES...")
        print("=" * 50)

        python_files = list(self.project_root.rglob("*.py"))
        print(f"📁 Archivos Python encontrados: {len(python_files)}")

        results = {
            'files_scanned': len(python_files),
            'files_modified': 0,
            'total_fixes': 0,
            'fixes_by_type': self.fixes_applied.copy()
        }

        for file_path in python_files:
            if self._should_skip_file(file_path):
                continue

            file_fixes = self._process_file(file_path, apply_fixes)
            if file_fixes > 0:
                results['files_modified'] += 1
                results['total_fixes'] += file_fixes

        # Actualizar contadores finales
        results['fixes_by_type'] = self.fixes_applied

        self._print_summary(results, apply_fixes)
        return results

    def _should_skip_file(self, file_path: Path) -> bool:
        """Determina si un archivo debe ser omitido."""
        skip_patterns = [
            '__pycache__', '.git', '.vscode', 'venv', 'env',
            '.pytest_cache', 'node_modules'
        ]

        str_path = str(file_path)
        return any(pattern in str_path for pattern in skip_patterns)

    def _process_file(self, file_path: Path, apply_fixes: bool) -> int:
        """Procesa un archivo individual y aplica fixes."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
        except Exception as e:
            print(f"❌ Error leyendo {file_path}: {e}")
            return 0

        modified_content = original_content
        fixes_in_file = 0

        # Fix 1: JSONDecodeError import
        if 'JSONDecodeError' in modified_content and 'from json import JSONDecodeError' not in modified_content:
            if modified_content.count('import json') > 0:
                modified_content = re.sub(
                    r'^import json$',
                    'import json\nfrom json import JSONDecodeError',
                    modified_content,
                    flags=re.MULTILINE
                )
                fixes_in_file += 1
                self.fixes_applied['json_decode_error'] += 1

        # Fix 2: Remove duplicate imports
        lines = modified_content.split('\n')
        seen_imports = set()
        filtered_lines = []

        for line in lines:
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                if line.strip() not in seen_imports:
                    seen_imports.add(line.strip())
                    filtered_lines.append(line)
                else:
                    fixes_in_file += 1
                    self.fixes_applied['duplicate_imports'] += 1
                    print(f"  🔧 Removiendo import duplicado: {line.strip()}")
            else:
                filtered_lines.append(line)

        modified_content = '\n'.join(filtered_lines)

        # Fix 3: Remove simple unused imports (solo los obvios)
        obvious_unused = [
            'import logging\n',
            'import sys\n',
            'import os\n',
            'import json\n'
        ]

        for unused_import in obvious_unused:
            if unused_import in modified_content:
                # Solo remover si no se usa en el archivo
                import_name = unused_import.split()[1].replace('\n', '')
                if not self._is_import_used(modified_content, import_name, unused_import):
                    modified_content = modified_content.replace(unused_import, '')
                    fixes_in_file += 1
                    self.fixes_applied['unused_imports'] += 1

        # Fix 4: Constant redefinition (comentar redefiniciones)
        constant_pattern = r'^([A-Z_]+)\s*=.*$'
        lines = modified_content.split('\n')
        seen_constants = set()

        for i, line in enumerate(lines):
            match = re.match(constant_pattern, line.strip())
            if match:
                constant_name = match.group(1)
                if constant_name in seen_constants:
                    lines[i] = f"# {line}  # Redefinition commented out"
                    fixes_in_file += 1
                    self.fixes_applied['constant_redefinition'] += 1
                else:
                    seen_constants.add(constant_name)

        modified_content = '\n'.join(lines)

        # Aplicar cambios si es necesario
        if fixes_in_file > 0 and apply_fixes:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(modified_content)
                print(f"✅ {file_path.name}: {fixes_in_file} fixes aplicados")
            except Exception as e:
                print(f"❌ Error escribiendo {file_path}: {e}")
                return 0
        elif fixes_in_file > 0:
            print(f"🔍 {file_path.name}: {fixes_in_file} fixes detectados (no aplicados)")

        return fixes_in_file

    def _is_import_used(self, content: str, import_name: str, import_line: str) -> bool:
        """Verifica si un import es usado en el archivo."""
        # Remover la línea del import para el análisis
        content_without_import = content.replace(import_line, '')

        # Buscar usos del import
        patterns = [
            rf'\b{import_name}\.',  # import_name.something
            rf'\b{import_name}\s*\(',  # import_name(
            rf'={import_name}\b',  # = import_name
            rf'\({import_name}\b',  # (import_name
        ]

        for pattern in patterns:
            if re.search(pattern, content_without_import):
                return True

        return False

    def _print_summary(self, results: Dict, applied: bool) -> None:
        """Imprime resumen de resultados."""
        action = "APLICADOS" if applied else "DETECTADOS"
        print(f"\n🎯 RESUMEN DE FIXES {action}:")
        print("=" * 40)
        print(f"📁 Archivos escaneados: {results['files_scanned']}")
        print(f"📝 Archivos modificados: {results['files_modified']}")
        print(f"🔧 Total de fixes: {results['total_fixes']}")
        print("\n📊 FIXES POR TIPO:")
        for fix_type, count in results['fixes_by_type'].items():
            if count > 0:
                print(f"  ✅ {fix_type.replace('_', ' ').title()}: {count}")


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(description="Quick Fixes para errores de Pylance")
    parser.add_argument("--scan", action="store_true", help="Solo escanear errores")
    parser.add_argument("--fix", action="store_true", help="Aplicar fixes")
    parser.add_argument("--all", action="store_true", help="Escanear y aplicar")

    args = parser.parse_args()

    if not any([args.scan, args.fix, args.all]):
        parser.print_help()
        return

    project_root = Path.cwd()
    fixer = QuickFixer(project_root)

    if args.all:
        # Primero escanear
        print("🔍 PASO 1: ESCANEANDO...")
        fixer.scan_and_fix_all(apply_fixes=False)

        # Luego aplicar
        input("\n⏸️  Presiona Enter para aplicar fixes...")
        print("\n🔧 PASO 2: APLICANDO FIXES...")
        fixer.scan_and_fix_all(apply_fixes=True)

    elif args.scan:
        fixer.scan_and_fix_all(apply_fixes=False)
    elif args.fix:
        fixer.scan_and_fix_all(apply_fixes=True)

    print("\n✅ Quick Fixes completado!")


if __name__ == "__main__":
    main()
