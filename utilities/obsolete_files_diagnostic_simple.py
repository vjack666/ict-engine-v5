#!/usr/bin/env python3
"""
🔍 OBSOLETE FILES DIAGNOSTIC SIMPLE - ICT Engine v5.0
====================================================

Sistema automático simplificado de diagnóstico para identificar archivos obsoletos.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple
import re
import json
from datetime import datetime

# Configurar paths
PROJECT_ROOT = Path(__file__).parent.parent

def log_message(level: str, message: str):
    """Log message simple"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")

class SimpleObsoleteDiagnostic:
    """Diagnosticador simplificado de archivos obsoletos"""

    def __init__(self):
        self.project_root = PROJECT_ROOT

    def scan_python_files(self) -> List[Path]:
        """Escanea todos los archivos Python del proyecto"""
        python_files = []
        for file_path in self.project_root.rglob("*.py"):
            if "__pycache__" not in str(file_path):
                python_files.append(file_path)
        return python_files

    def identify_obsolete_candidates(self) -> Dict[str, List[str]]:
        """Identifica candidatos obsoletos por categorías"""
        all_files = self.scan_python_files()

        candidates = {
            'backup_files': [],
            'fixed_files': [],
            'test_debug_files': [],
            'deprecated_files': [],
            'migration_temp_files': [],
            'broken_reference_files': []
        }

        # Referencias conocidas como rotas
        broken_imports = [
            'utils.advanced_candle_downloader',
            'utils.candle_integration',
            'utils.auto_data_initializer',
            'utils.simple_auto_downloader'
        ]

        for file_path in all_files:
            relative_path = str(file_path.relative_to(self.project_root))
            file_name = file_path.name.lower()

            # Verificar patrones obsoletos
            if any(keyword in file_name for keyword in ['backup', '_bak', 'deprecated', 'old']):
                candidates['backup_files'].append(relative_path)

            elif 'fixed' in file_name:
                candidates['fixed_files'].append(relative_path)

            elif any(keyword in file_name for keyword in ['test_', 'testing_', 'verify_', 'diagnose_']):
                candidates['test_debug_files'].append(relative_path)

            elif any(keyword in relative_path.lower() for keyword in ['deprecated', 'legacy']):
                candidates['deprecated_files'].append(relative_path)

            elif 'migration' in relative_path and any(keyword in file_name for keyword in ['simple', 'temp', 'fix']):
                candidates['migration_temp_files'].append(relative_path)

            # Verificar referencias rotas
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                for broken_import in broken_imports:
                    if broken_import in content:
                        candidates['broken_reference_files'].append(relative_path)
                        break

            except Exception as e:
                log_message("WARNING", f"Error leyendo {relative_path}: {e}")

        return candidates

    def classify_safety_level(self, candidates: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """Clasifica archivos por nivel de seguridad para eliminación"""
        classification = {
            'safe_to_delete': [],
            'review_before_delete': [],
            'keep_files': []
        }

        # Archivos críticos que nunca se deben eliminar
        critical_patterns = [
            'main.py',
            'mt5_data_manager.py',
            'dashboard_definitivo.py',
            'logging_interface.py',
            'config_manager.py'
        ]

        # Archivos seguros para eliminar
        safe_categories = ['backup_files', 'fixed_files']

        # Archivos que requieren revisión
        review_categories = ['test_debug_files', 'migration_temp_files', 'broken_reference_files']

        for category, files in candidates.items():
            for file_path in files:
                # Verificar si es archivo crítico
                if any(critical in file_path for critical in critical_patterns):
                    classification['keep_files'].append(file_path)
                elif category in safe_categories:
                    classification['safe_to_delete'].append(file_path)
                else:
                    classification['review_before_delete'].append(file_path)

        return classification

    def run_diagnostic(self) -> Dict:
        """Ejecuta diagnóstico completo"""
        log_message("INFO", "🔍 Iniciando diagnóstico de archivos obsoletos...")

        # Identificar candidatos
        candidates = self.identify_obsolete_candidates()

        # Clasificar por seguridad
        classification = self.classify_safety_level(candidates)

        # Calcular estadísticas
        total_candidates = sum(len(files) for files in candidates.values())

        results = {
            'timestamp': datetime.now().isoformat(),
            'total_python_files': len(self.scan_python_files()),
            'total_obsolete_candidates': total_candidates,
            'categories': candidates,
            'safety_classification': classification,
            'summary': {
                'safe_to_delete': len(classification['safe_to_delete']),
                'review_before_delete': len(classification['review_before_delete']),
                'keep_files': len(classification['keep_files'])
            }
        }

        return results

    def print_report(self, results: Dict):
        """Imprime reporte de diagnóstico"""
        log_message("INFO", "=" * 60)
        log_message("INFO", "📊 REPORTE DE ARCHIVOS OBSOLETOS")
        log_message("INFO", "=" * 60)

        summary = results['summary']
        log_message("INFO", f"📁 Total archivos Python: {results['total_python_files']}")
        log_message("INFO", f"🗑️ Candidatos obsoletos: {results['total_obsolete_candidates']}")
        log_message("INFO", f"✅ Seguros para eliminar: {summary['safe_to_delete']}")
        log_message("INFO", f"⚠️ Revisar antes de eliminar: {summary['review_before_delete']}")
        log_message("INFO", f"🛡️ Mantener (críticos): {summary['keep_files']}")

        # Detalles por categoría
        log_message("INFO", "\n📋 CATEGORÍAS DE ARCHIVOS OBSOLETOS:")
        for category, files in results['categories'].items():
            if files:
                log_message("INFO", f"\n{category.upper().replace('_', ' ')} ({len(files)} archivos):")
                for file_path in files[:5]:  # Mostrar solo primeros 5
                    log_message("INFO", f"  - {file_path}")
                if len(files) > 5:
                    log_message("INFO", f"  ... y {len(files) - 5} más")

        # Archivos seguros para eliminar
        safe_files = results['safety_classification']['safe_to_delete']
        if safe_files:
            log_message("INFO", "\n✅ ARCHIVOS SEGUROS PARA ELIMINAR:")
            for file_path in safe_files:
                log_message("INFO", f"  - {file_path}")

        # Archivos que requieren revisión
        review_files = results['safety_classification']['review_before_delete']
        if review_files:
            log_message("INFO", "\n⚠️ ARCHIVOS QUE REQUIEREN REVISIÓN:")
            for file_path in review_files[:10]:  # Mostrar solo primeros 10
                log_message("INFO", f"  - {file_path}")
            if len(review_files) > 10:
                log_message("INFO", f"  ... y {len(review_files) - 10} más")

    def save_report(self, results: Dict) -> Path:
        """Guarda reporte en JSON"""
        output_dir = self.project_root / "docs" / "reports"
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = output_dir / f"obsolete_files_simple_{timestamp}.json"

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        log_message("INFO", f"📊 Reporte guardado en: {output_path}")
        return output_path

    def execute_safe_cleanup(self, results: Dict) -> int:
        """Ejecuta limpieza segura de archivos obsoletos"""
        safe_files = results['safety_classification']['safe_to_delete']
        deleted_count = 0

        log_message("INFO", f"🧹 Iniciando limpieza de {len(safe_files)} archivos seguros...")

        for file_path in safe_files:
            full_path = self.project_root / file_path
            try:
                if full_path.exists():
                    full_path.unlink()
                    log_message("INFO", f"✅ Eliminado: {file_path}")
                    deleted_count += 1
                else:
                    log_message("WARNING", f"⚠️ No encontrado: {file_path}")
            except Exception as e:
                log_message("ERROR", f"❌ Error eliminando {file_path}: {e}")

        log_message("INFO", f"🎉 Limpieza completada: {deleted_count} archivos eliminados")
        return deleted_count

def main():
    """Función principal"""
    log_message("INFO", "🔍 OBSOLETE FILES DIAGNOSTIC SIMPLE - ICT Engine v5.0")
    log_message("INFO", f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Crear diagnosticador
    diagnostic = SimpleObsoleteDiagnostic()

    # Ejecutar diagnóstico
    results = diagnostic.run_diagnostic()

    # Mostrar reporte
    diagnostic.print_report(results)

    # Guardar reporte
    report_path = diagnostic.save_report(results)

    # Preguntar si ejecutar limpieza
    if results['summary']['safe_to_delete'] > 0:
        log_message("INFO", "\n🧹 OPCIONES DE LIMPIEZA:")
        log_message("INFO", "Para ejecutar limpieza automática de archivos seguros:")
        log_message("INFO", f"python utilities/obsolete_files_diagnostic_simple.py --cleanup")

    return results

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cleanup":
        log_message("INFO", "🧹 Ejecutando limpieza automática...")
        diagnostic = SimpleObsoleteDiagnostic()
        results = diagnostic.run_diagnostic()
        deleted = diagnostic.execute_safe_cleanup(results)
        log_message("INFO", f"✨ Proceso completado: {deleted} archivos eliminados")
    else:
        main()
