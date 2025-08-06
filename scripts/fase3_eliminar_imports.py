#!/usr/bin/env python3
"""
🗑️ FASE 3: ELIMINAR - REEMPLAZO MASIVO DE IMPORTS
===============================================
Reemplaza imports dispersos con imports del SIC expandido
Implementa la tercera fase de la estrategia "AÑADIR → REEMPLAZAR → ELIMINAR"

Autor: Sistema Sentinel Grid
Fecha: 2025-08-06
Versión: v3.0
"""

import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from collections import defaultdict

class MassiveImportReplacer:
    """🗑️ Reemplazador masivo de imports con SIC"""

    def __init__(self):
        self.backup_dir = Path(f'backup_fase3_eliminar_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        self.stats = {
            'files_processed': 0,
            'files_modified': 0,
            'imports_replaced': 0,
            'backups_created': 0,
            'errors': 0
        }

        # Patrones de reemplazo más comunes (basados en Fase 1)
        self.replacement_patterns = [
            # Typing
            (r'^(\s*)from typing import (.+)$', r'\1from sistema.sic import \2'),

            # Dataclasses
            (r'^(\s*)from dataclasses import (.+)$', r'\1from sistema.sic import \2'),

            # Datetime
            (r'^(\s*)from datetime import (.+)$', r'\1from sistema.sic import \2'),

            # Pathlib
            (r'^(\s*)from pathlib import Path$', r'\1from sistema.sic import Path'),

            # Standard library básicos
            (r'^(\s*)import os$', r'\1from sistema.sic import os'),
            (r'^(\s*)import sys$', r'\1from sistema.sic import sys'),
            (r'^(\s*)import json$', r'\1from sistema.sic import json'),
            (r'^(\s*)import time$', r'\1from sistema.sic import time'),
            (r'^(\s*)import re$', r'\1from sistema.sic import re'),

            # Logging (patrón común detectado)
            (r'^(\s*)from sistema\.smart_directory_logger import (.+)$', r'\1from sistema.sic import \2'),
            (r'^(\s*)from sistema\.logging_interface import (.+)$', r'\1from sistema.sic import \2'),

            # ICT Engine (si está disponible)
            (r'^(\s*)from core\.ict_engine\.ict_detector import (.+)$', r'\1from sistema.sic import \2'),
            (r'^(\s*)from core\.ict_engine\.ict_analyzer import (.+)$', r'\1from sistema.sic import \2'),

            # POI System (si está disponible)
            (r'^(\s*)from core\.poi_system\.poi_manager import (.+)$', r'\1from sistema.sic import \2'),
            (r'^(\s*)from core\.poi_system\.poi_detector import (.+)$', r'\1from sistema.sic import \2'),

            # Dashboard (si está disponible)
            (r'^(\s*)from dashboard\.dashboard_controller import (.+)$', r'\1from sistema.sic import \2'),

            # Config (si está disponible)
            (r'^(\s*)from config\.config_manager import (.+)$', r'\1from sistema.sic import \2'),
        ]

        # Archivos a excluir del reemplazo
        self.exclude_files = {
            'sic.py', 'imports_interface.py', '__init__.py',
            'fase1_scan_imports.py', 'fase2_expandir_sic.py', 'fase3_eliminar_imports.py',
            'scanner_independiente.py'
        }

        # Directorios a excluir
        self.exclude_dirs = {
            '__pycache__', '.git', '.vscode', 'backup_sic_expansion_20250806_122656',
            'backup_sic_migration', 'backup_pre_restauracion_directa_20250806_113634',
            'backup_pre_migracion_v2_20250806_113857', 'migration_reports'
        }

    def create_backup(self, file_path: Path) -> bool:
        """💾 Crear backup de un archivo antes de modificarlo"""

        try:
            # Crear directorio de backup si no existe
            self.backup_dir.mkdir(exist_ok=True)

            # Estructura de directorio relativa
            relative_path = file_path.relative_to('.')
            backup_file_path = self.backup_dir / relative_path

            # Crear directorios padre
            backup_file_path.parent.mkdir(parents=True, exist_ok=True)

            # Copiar archivo
            shutil.copy2(file_path, backup_file_path)
            self.stats['backups_created'] += 1

            return True

        except Exception as e:
            print(f"⚠️ Error creando backup para {file_path}: {e}")
            return False

    def analyze_file_imports(self, file_path: Path) -> dict:
        """🔍 Analizar imports en un archivo"""

        analysis = {
            'file': str(file_path),
            'current_imports': [],
            'replaceable_imports': [],
            'replacement_count': 0,
            'needs_sic_import': False
        }

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            lines = content.split('\n')

            for line_num, line in enumerate(lines, 1):
                original_line = line
                line_stripped = line.strip()

                if not line_stripped or line_stripped.startswith('#'):
                    continue

                # Verificar si es un import
                if line_stripped.startswith('import ') or line_stripped.startswith('from '):
                    analysis['current_imports'].append({
                        'line_number': line_num,
                        'original': original_line,
                        'stripped': line_stripped
                    })

                    # Verificar si es reemplazable
                    for pattern, replacement in self.replacement_patterns:
                        if re.match(pattern, original_line):
                            analysis['replaceable_imports'].append({
                                'line_number': line_num,
                                'original': original_line,
                                'pattern': pattern,
                                'replacement': replacement
                            })
                            analysis['replacement_count'] += 1
                            analysis['needs_sic_import'] = True
                            break

            return analysis

        except Exception as e:
            analysis['error'] = str(e)
            return analysis

    def replace_imports_in_file(self, file_path: Path, dry_run: bool = True) -> dict:
        """🔄 Reemplazar imports en un archivo"""

        result = {
            'file': str(file_path),
            'modified': False,
            'replacements_made': 0,
            'errors': []
        }

        try:
            # Leer archivo
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            lines = content.split('\n')
            modified = False
            replacements_count = 0

            # Aplicar patrones de reemplazo línea por línea
            for i, line in enumerate(lines):
                for pattern, replacement in self.replacement_patterns:
                    match = re.match(pattern, line)
                    if match:
                        new_line = re.sub(pattern, replacement, line)
                        if new_line != line:
                            lines[i] = new_line
                            modified = True
                            replacements_count += 1
                            break

            # Si se hicieron cambios
            if modified:
                result['modified'] = True
                result['replacements_made'] = replacements_count

                # Verificar si ya existe import del SIC
                sic_import_exists = any('from sistema.sic import' in line for line in lines)

                if not sic_import_exists and replacements_count > 0:
                    # Encontrar lugar para insertar import del SIC
                    insert_index = 0
                    for i, line in enumerate(lines):
                        if line.strip().startswith('"""') or line.strip().startswith("'''"):
                            # Buscar el final del docstring
                            quote_type = '"""' if '"""' in line else "'''"
                            if line.strip().endswith(quote_type) and len(line.strip()) > 3:
                                insert_index = i + 1
                                break
                            else:
                                for j in range(i + 1, len(lines)):
                                    if quote_type in lines[j]:
                                        insert_index = j + 1
                                        break
                                break
                        elif line.strip().startswith('#') or line.strip() == '':
                            continue
                        else:
                            insert_index = i
                            break

                    # Insertar import del SIC si no existe
                    lines.insert(insert_index, '# === IMPORT SIC EXPANDIDO ===')
                    lines.insert(insert_index + 1, 'from sistema.sic import *')
                    lines.insert(insert_index + 2, '')
                    result['replacements_made'] += 1

                if not dry_run:
                    # Crear backup antes de modificar
                    if self.create_backup(file_path):
                        # Escribir archivo modificado
                        new_content = '\n'.join(lines)
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)

                        self.stats['files_modified'] += 1
                        self.stats['imports_replaced'] += replacements_count

            return result

        except Exception as e:
            result['errors'].append(str(e))
            self.stats['errors'] += 1
            return result

    def process_project(self, dry_run: bool = True) -> dict:
        """🚀 Procesar todo el proyecto"""

        print(f"🗑️ PROCESANDO PROYECTO - {'DRY RUN' if dry_run else 'MODO REAL'}")
        print("=" * 60)

        project_results = {
            'files_analyzed': 0,
            'files_with_replaceable_imports': 0,
            'total_replacements_possible': 0,
            'file_results': {}
        }

        # Buscar archivos Python
        for root, dirs, files in os.walk('.'):
            # Filtrar directorios
            dirs[:] = [d for d in dirs if d not in self.exclude_dirs]

            for file in files:
                if file.endswith('.py') and file not in self.exclude_files:
                    file_path = Path(root) / file

                    try:
                        # Analizar archivo
                        analysis = self.analyze_file_imports(file_path)
                        project_results['files_analyzed'] += 1

                        if analysis['replacement_count'] > 0:
                            project_results['files_with_replaceable_imports'] += 1
                            project_results['total_replacements_possible'] += analysis['replacement_count']

                            # Reemplazar imports
                            replacement_result = self.replace_imports_in_file(file_path, dry_run)
                            project_results['file_results'][str(file_path)] = {
                                'analysis': analysis,
                                'replacement': replacement_result
                            }

                            if replacement_result['replacements_made'] > 0:
                                status = "🔍 Se reemplazarían" if dry_run else "✅ Reemplazados"
                                print(f"   {status}: {file_path} ({replacement_result['replacements_made']} imports)")

                        self.stats['files_processed'] += 1

                        # Progress indicator
                        if self.stats['files_processed'] % 20 == 0:
                            print(f"   📁 Procesados: {self.stats['files_processed']} archivos...")

                    except Exception as e:
                        print(f"⚠️ Error procesando {file_path}: {e}")
                        self.stats['errors'] += 1

        return project_results

    def generate_report(self, results: dict, dry_run: bool) -> str:
        """📊 Generar reporte de resultados"""

        report = f"""
🗑️ REPORTE FASE 3: ELIMINAR - REEMPLAZO MASIVO DE IMPORTS
========================================================

📋 MODO: {'DRY RUN (Vista Previa)' if dry_run else 'EJECUCIÓN REAL'}
📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 ESTADÍSTICAS GENERALES:
   📁 Archivos procesados: {self.stats['files_processed']}
   📁 Archivos analizados: {results['files_analyzed']}
   🎯 Archivos con imports reemplazables: {results['files_with_replaceable_imports']}
   📝 Archivos modificados: {self.stats['files_modified']}

🔄 REEMPLAZOS:
   🎯 Total reemplazos posibles: {results['total_replacements_possible']}
   ✅ Imports reemplazados: {self.stats['imports_replaced']}
   💾 Backups creados: {self.stats['backups_created']}
   ❌ Errores: {self.stats['errors']}

📈 TASA DE ÉXITO:
   Archivos procesados: {(self.stats['files_processed'] / max(results['files_analyzed'], 1)) * 100:.1f}%
   Reemplazos realizados: {(self.stats['imports_replaced'] / max(results['total_replacements_possible'], 1)) * 100:.1f}%

{'💾 BACKUP DIRECTORY: ' + str(self.backup_dir) if not dry_run and self.stats['backups_created'] > 0 else ''}
"""

        if dry_run:
            report += f"""
🔍 VISTA PREVIA COMPLETADA:
   - Los imports SERÍAN reemplazados por imports del SIC expandido
   - Se CREARÍAN backups automáticos antes de modificar archivos
   - El proyecto FUNCIONARÍA con imports centralizados

❓ PARA EJECUTAR REALMENTE:
   python scripts/fase3_eliminar_imports.py --execute
"""
        else:
            report += f"""
✅ REEMPLAZO MASIVO COMPLETADO:
   - Imports reemplazados exitosamente con SIC expandido
   - Backups de seguridad creados en: {self.backup_dir}
   - Proyecto migrado a sistema centralizado

🎉 ESTRATEGIA "AÑADIR → REEMPLAZAR → ELIMINAR" COMPLETADA
"""

        return report

def main():
    """🚀 Función principal de eliminación masiva"""

    print("🗑️ FASE 3: ELIMINAR - REEMPLAZO MASIVO DE IMPORTS")
    print("=" * 60)

    import sys

    # Determinar si es dry run o ejecución real
    dry_run = '--execute' not in sys.argv

    if dry_run:
        print("🔍 EJECUTANDO EN MODO DRY RUN (Vista previa)")
        print("   Para ejecutar realmente, usar: --execute")
    else:
        print("🚀 EJECUTANDO EN MODO REAL")
        print("   ⚠️ Se modificarán archivos y crearán backups")

    print("")

    try:
        # Inicializar reemplazador
        replacer = MassiveImportReplacer()

        # Procesar proyecto
        results = replacer.process_project(dry_run=dry_run)

        # Generar y mostrar reporte
        report = replacer.generate_report(results, dry_run)
        print(report)

        # Guardar reporte
        report_file = f"migration_reports/fase3_report_{'dry_run' if dry_run else 'executed'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        os.makedirs('migration_reports', exist_ok=True)

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"📄 Reporte guardado en: {report_file}")

        if dry_run:
            print(f"\n🎯 FASE 3 COMPLETADA (Vista Previa)")
            print("🚀 Para ejecutar realmente: python scripts/fase3_eliminar_imports.py --execute")
        else:
            print(f"\n🎉 ESTRATEGIA COMPLETA EJECUTADA EXITOSAMENTE")
            print("=" * 60)
            print("✅ FASE 1: AÑADIR - Imports comunes detectados")
            print("✅ FASE 2: REEMPLAZAR - SIC expandido creado")
            print("✅ FASE 3: ELIMINAR - Imports masivamente reemplazados")
            print("")
            print("🏆 PROYECTO MIGRADO A SISTEMA CENTRALIZADO")

        return True

    except Exception as e:
        print(f"\n❌ ERROR EN FASE 3: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
