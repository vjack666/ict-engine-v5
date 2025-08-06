"""
🔧 SCRIPT DE MIGRACIÓN AUTOMÁTICA AL SIC
=======================================

Convierte archivos del sistema actual al Sistema de Imports Centralizado.
Automatiza la migración siguiendo el patrón exitoso del SLUC.

Autor: Sistema Sentinel Grid
Fecha: 2025-08-06
Versión: v1.0
"""

from sistema.sic import re
from sistema.sic import os
import shutil
from sistema.sic import Path
from sistema.sic import Dict, List, Tuple, Optional
from sistema.sic import datetime

class SICMigrator:
    """Migrador automático al Sistema de Imports Centralizado"""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.backup_dir = self.project_root / "backup_sic_migration"

        # Patrones de imports a reemplazar
        self.replacement_patterns = {
            # Tipos comunes
            r'from typing import.*': 'from sistema.imports_interface import Dict, List, Optional, Tuple, Any, Union',
            r'from dataclasses import.*': 'from sistema.imports_interface import dataclass, field, asdict',
            r'from datetime import.*': 'from sistema.imports_interface import datetime, timedelta, timezone',
            r'from pathlib import.*': 'from sistema.imports_interface import Path',
            r'import asyncio': 'from sistema.imports_interface import asyncio',
            r'import json': 'from sistema.imports_interface import json',
            r'import time': 'from sistema.imports_interface import time',
            r'import sys': 'from sistema.imports_interface import sys',
            r'import os': 'from sistema.imports_interface import os',
            r'import re': 'from sistema.imports_interface import re',

            # ICT Engine
            r'from core\.ict_engine\.ict_engine import.*': 'from sistema.imports_interface import get_ict_engine',
            r'from core\.ict_engine\.ict_detector import.*': 'from sistema.imports_interface import get_ict_detector',
            r'from core\.ict_engine\.ict_types import.*': 'from sistema.imports_interface import ICTPattern, TradingDirection, SessionType, PATTERN_EMOJIS',
            r'from core\.ict_engine\.confidence_engine import.*': '# ICT Engine via SIC',
            r'from core\.ict_engine\..*': '# ICT Engine via SIC',

            # POI System
            r'from core\.poi_system\..*': 'from sistema.imports_interface import get_poi_system, get_poi_detector',

            # Dashboard
            r'from dashboard\.dashboard_definitivo import.*': 'from sistema.imports_interface import get_dashboard',
            r'from dashboard\.dashboard_controller import.*': 'from sistema.imports_interface import get_dashboard_controller',
            r'from dashboard\..*': '# Dashboard via SIC',

            # Sistema (logging)
            r'from sistema\.logging_interface import.*': 'from sistema.imports_interface import get_logging, enviar_senal_log, log_info, log_error',

            # Utils
            r'from utils\.mt5_data_manager import.*': 'from sistema.imports_interface import get_mt5_manager',
            r'from utils\..*': '# Utils via SIC',

            # Data Management
            r'from core\.data_management\..*': 'from sistema.imports_interface import get_candle_downloader',

            # Analysis Command Center
            r'from core\.analysis_command_center\..*': 'from sistema.imports_interface import get_analysis_orchestrator'
        }

    def create_backup(self, file_path: Path) -> Path:
        """Crea backup de un archivo antes de la migración"""
        self.backup_dir.mkdir(exist_ok=True)

        # Mantener estructura de directorios
        relative_path = file_path.relative_to(self.project_root)
        backup_path = self.backup_dir / relative_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)

        # Agregar timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_path.with_suffix(f'.{timestamp}.bak')

        shutil.copy2(file_path, backup_path)
        return backup_path

    def analyze_imports(self, content: str) -> Tuple[List[str], List[str]]:
        """Analiza los imports de un archivo y identifica cuáles migrar"""
        lines = content.split('\n')
        import_lines = []
        other_lines = []

        for line in lines:
            stripped = line.strip()
            if (stripped.startswith('import ') or
                stripped.startswith('from ') and ' import ' in stripped):
                import_lines.append(line)
            else:
                other_lines.append(line)

        return import_lines, other_lines

    def apply_sic_patterns(self, import_lines: List[str]) -> List[str]:
        """Aplica los patrones de migración al SIC"""
        migrated_lines = []
        sic_imports = set()

        for line in import_lines:
            migrated = False

            for pattern, replacement in self.replacement_patterns.items():
                if re.search(pattern, line):
                    if not replacement.startswith('#'):
                        sic_imports.add(replacement)
                    migrated = True
                    break

            if not migrated:
                # Mantener imports que no necesitan migración
                migrated_lines.append(line)

        # Agregar imports del SIC consolidados
        if sic_imports:
            # Consolidar imports similares
            consolidated = self.consolidate_sic_imports(sic_imports)
            migrated_lines = consolidated + migrated_lines

        return migrated_lines

    def consolidate_sic_imports(self, sic_imports: set) -> List[str]:
        """Consolida múltiples imports del SIC en líneas optimizadas"""
        # Separar por tipo de import
        basic_types = []
        functions = []
        classes = []

        for imp in sic_imports:
            if any(t in imp for t in ['Dict', 'List', 'Optional', 'dataclass', 'datetime']):
                # Extraer elementos específicos
                if 'import ' in imp:
                    items = imp.split('import ')[1].split(', ')
                    basic_types.extend(items)
            elif 'get_' in imp:
                if 'import ' in imp:
                    items = imp.split('import ')[1].split(', ')
                    functions.extend(items)
            else:
                if 'import ' in imp:
                    items = imp.split('import ')[1].split(', ')
                    classes.extend(items)

        # Crear imports consolidados
        consolidated = []

        if basic_types:
            unique_types = list(set(basic_types))
            consolidated.append(f"from sistema.imports_interface import {', '.join(unique_types)}")

        if functions:
            unique_functions = list(set(functions))
            consolidated.append(f"from sistema.imports_interface import {', '.join(unique_functions)}")

        if classes:
            unique_classes = list(set(classes))
            consolidated.append(f"from sistema.imports_interface import {', '.join(unique_classes)}")

        return consolidated

    def migrate_file(self, file_path: Path, dry_run: bool = False) -> bool:
        """Migra un archivo individual al SIC"""
        try:
            # Leer contenido original
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            # Analizar imports
            import_lines, other_lines = self.analyze_imports(original_content)

            if not import_lines:
                return False  # No hay imports que migrar

            # Aplicar patrones de migración
            migrated_imports = self.apply_sic_patterns(import_lines)

            # Reconstruir contenido
            new_content_lines = []

            # Agregar header del archivo si existe
            content_lines = original_content.split('\n')
            header_end = 0

            for i, line in enumerate(content_lines):
                if line.strip().startswith('"""') or line.strip().startswith("'''"):
                    # Encontrar el final del docstring
                    quote_type = '"""' if '"""' in line else "'''"
                    quote_count = line.count(quote_type)
                    if quote_count >= 2:
                        header_end = i + 1
                        break
                    else:
                        # Buscar cierre en líneas siguientes
                        for j in range(i + 1, len(content_lines)):
                            if quote_type in content_lines[j]:
                                header_end = j + 1
                                break
                        break
                elif line.strip() and not (line.strip().startswith('import ') or
                                         (line.strip().startswith('from ') and ' import ' in line)):
                    break

            # Agregar header
            new_content_lines.extend(content_lines[:header_end])

            # Agregar imports migrados
            if migrated_imports:
                new_content_lines.append('')  # Línea en blanco
                new_content_lines.extend(migrated_imports)
                new_content_lines.append('')  # Línea en blanco

            # Agregar resto del contenido (sin imports originales)
            rest_start = header_end
            while rest_start < len(content_lines):
                line = content_lines[rest_start]
                if not (line.strip().startswith('import ') or
                       (line.strip().startswith('from ') and ' import ' in line)):
                    break
                rest_start += 1

            new_content_lines.extend(content_lines[rest_start:])

            # Nuevo contenido
            new_content = '\n'.join(new_content_lines)

            if not dry_run:
                # Crear backup
                backup_path = self.create_backup(file_path)
                print(f"💾 Backup: {backup_path}")

                # Escribir archivo migrado
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                print(f"✅ Migrado: {file_path.relative_to(self.project_root)}")
            else:
                print(f"🔍 Sería migrado: {file_path.relative_to(self.project_root)}")
                print(f"   Imports originales: {len(import_lines)}")
                print(f"   Imports migrados: {len(migrated_imports)}")

            return True

        except Exception as e:
            print(f"❌ Error migrando {file_path}: {e}")
            return False

def main():
    """Función principal del migrador"""
    from sistema.sic import sys

    project_root = Path(__file__).parent.parent
    migrator = SICMigrator(str(project_root))

    # Determinar modo de ejecución
    dry_run_mode = '--dry-run' in sys.argv
    target_file = None

    # Verificar si se especifica un archivo específico
    for arg in sys.argv[1:]:
        if not arg.startswith('--'):
            target_file = arg
            break

    print("🔧 MIGRADOR AL SISTEMA DE IMPORTS CENTRALIZADO (SIC)")
    print("=" * 60)

    if target_file:
        # Migrar archivo específico
        file_path = project_root / target_file
        if file_path.exists():
            print(f"\n🎯 Migrando archivo específico: {target_file}")
            success = migrator.migrate_file(file_path, dry_run=dry_run_mode)
            if success and not dry_run_mode:
                print(f"✅ Migración completada: {target_file}")
            elif success and dry_run_mode:
                print(f"🔍 Migración simulada: {target_file}")
        else:
            print(f"❌ Archivo no encontrado: {target_file}")
    else:
        # Migrar archivos de alta prioridad por defecto
        priority_files = [
            "dashboard/dashboard_definitivo.py",
            "core/ict_engine/ict_detector.py",
            "dashboard/dashboard_widgets.py",
            "core/analysis_command_center/tct_pipeline/tct_interface.py",
            "core/analytics/ict_analyzer.py",
            "core/data_management/advanced_candle_downloader.py",
            "dashboard/hibernation_widget_v2.py",
            "dashboard/poi_dashboard_integration.py"
        ]

        print(f"\n{'🧪 MODO DRY-RUN' if dry_run_mode else '🚀 MODO MIGRACIÓN REAL'}")
        print(f"Archivos a procesar: {len(priority_files)}")

        successful_migrations = 0
        failed_migrations = 0

        for file_rel_path in priority_files:
            file_path = project_root / file_rel_path
            if file_path.exists():
                print(f"\n🎯 Procesando: {file_rel_path}")
                success = migrator.migrate_file(file_path, dry_run=dry_run_mode)
                if success:
                    successful_migrations += 1
                else:
                    failed_migrations += 1
            else:
                print(f"⚠️  Archivo no encontrado: {file_rel_path}")
                failed_migrations += 1

        # Reporte final
        print(f"\n{'='*60}")
        print("📊 REPORTE FINAL DE MIGRACIÓN")
        print(f"{'='*60}")
        print(f"✅ Migraciones exitosas: {successful_migrations}")
        print(f"❌ Fallos: {failed_migrations}")
        print(f"📊 Tasa de éxito: {(successful_migrations/(successful_migrations+failed_migrations))*100:.1f}%")

        if not dry_run_mode and successful_migrations > 0:
            print(f"\n🎉 ¡{successful_migrations} archivos migrados al SIC exitosamente!")
            print(f"💾 Backups creados en: {migrator.backup_dir}")
            print(f"\n🔍 Ejecuta el análisis para ver la mejora:")
            print(f"   python scripts/fix_unused_imports.py --dry-run")

if __name__ == "__main__":
    main()
