#!/usr/bin/env python3
"""
🔍 OBSOLETE FILES DIAGNOSTIC - ICT Engine v5.0
=============================================

Sistema automático de diagnóstico para identificar archivos obsoletos,
referencias rotas y dependencias innecesarias.

Autor: Sistema de Diagnóstico Automático
Fecha: 03 Agosto 2025
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple
import re
import json
from datetime import datetime
from sistema.logging_interface import enviar_senal_log

# Configurar paths
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def log_message(level: str, message: str, component: str = "diagnostic"):
    """Log message simple"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")

class ObsoleteFilesDiagnostic:
    """Diagnosticador de archivos obsoletos"""

    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.obsolete_files = []
        self.broken_references = []
        self.analysis_results = {}

    def scan_project_files(self) -> List[Path]:
        """Escanea todos los archivos Python del proyecto"""
        python_files = []
        for file_path in self.project_root.rglob("*.py"):
            if "__pycache__" not in str(file_path):
                python_files.append(file_path)
        return python_files

    def identify_obsolete_patterns(self, file_path: Path) -> Dict[str, bool]:
        """Identifica patrones que indican archivos obsoletos"""
        patterns = {
            'is_backup': any(keyword in file_path.name.lower()
                           for keyword in ['backup', 'deprecated', 'old', '_bak']),
            'is_fixed_version': 'fixed' in file_path.name.lower(),
            'is_test_script': any(keyword in file_path.name.lower()
                                for keyword in ['test_', 'testing_', 'verify_']),
            'is_debug_temp': 'debug' in str(file_path) and any(keyword in file_path.name.lower()
                                                             for keyword in ['temp', 'fix', 'verify']),
            'is_sprint_executor': 'sprint' in str(file_path) and 'executor' in file_path.name.lower(),
            'is_migration_temp': 'migration' in str(file_path) and any(keyword in file_path.name.lower()
                                                                      for keyword in ['simple', 'temp', 'fix'])
        }
        return patterns

    def check_broken_references(self, file_path: Path) -> List[str]:
        """Verifica referencias rotas en un archivo"""
        broken_refs = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Referencias conocidas como rotas
            broken_imports = [
                'utils.advanced_candle_downloader',
                'utils.candle_integration',
                'utils.auto_data_initializer',
                'utils.simple_auto_downloader'
            ]

            for broken_import in broken_imports:
                if broken_import in content:
                    broken_refs.append(broken_import)

        except Exception as e:
                        enviar_senal_log("WARNING", f"Error leyendo {file_path}: {e}", "obsolete_diagnostic", "scan")

        return broken_refs

    def analyze_file_usage(self, file_path: Path) -> Dict[str, any]:
        """Analiza el uso de un archivo en el proyecto"""
        relative_path = file_path.relative_to(self.project_root)
        module_name = str(relative_path).replace('/', '.').replace('\\', '.').replace('.py', '')

        # Buscar referencias a este archivo en otros archivos
        references = []
        all_files = self.scan_project_files()

        for other_file in all_files:
            if other_file == file_path:
                continue

            try:
                with open(other_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Buscar imports de este módulo
                import_patterns = [
                    f"from {module_name} import",
                    f"import {module_name}",
                    f"from {module_name.replace('.', '/')}",
                    file_path.name.replace('.py', '')
                ]

                for pattern in import_patterns:
                    if pattern in content:
                        references.append(str(other_file.relative_to(self.project_root)))
                        break

            except Exception:
                continue

        return {
            'references_count': len(references),
            'referenced_by': references,
            'is_referenced': len(references) > 0
        }

    def classify_file_importance(self, file_path: Path) -> str:
        """Clasifica la importancia de un archivo"""
        relative_path = str(file_path.relative_to(self.project_root))

        # Archivos críticos que nunca se deben eliminar
        critical_files = [
            'main.py',
            'utils/mt5_data_manager.py',
            'dashboard/dashboard_definitivo.py',
            'sistema/logging_interface.py',
            'config/config_manager.py'
        ]

        # Directorios core
        core_dirs = ['core/', 'sistema/', 'config/']

        if relative_path in critical_files:
            return 'CRITICAL'
        elif any(relative_path.startswith(core_dir) for core_dir in core_dirs):
            return 'CORE'
        elif 'debug' in relative_path or 'testing' in relative_path:
            return 'DEBUG'
        elif 'utilities' in relative_path:
            return 'UTILITY'
        elif 'scripts' in relative_path:
            return 'SCRIPT'
        else:
            return 'UNKNOWN'

    def run_diagnostic(self) -> Dict[str, any]:
        """Ejecuta diagnóstico completo"""
        enviar_senal_log("INFO", "🔍 Iniciando diagnóstico de archivos obsoletos...", "obsolete_diagnostic", "scan")

        all_files = self.scan_project_files()
        results = {
            'total_files': len(all_files),
            'obsolete_candidates': [],
            'broken_references': [],
            'critical_files': [],
            'safe_to_delete': [],
            'requires_review': [],
            'analysis_timestamp': datetime.now().isoformat()
        }

        for file_path in all_files:
            # Análisis de patrones obsoletos
            obsolete_patterns = self.identify_obsolete_patterns(file_path)

            # Verificar referencias rotas
            broken_refs = self.check_broken_references(file_path)

            # Analizar uso del archivo
            usage_analysis = self.analyze_file_usage(file_path)

            # Clasificar importancia
            importance = self.classify_file_importance(file_path)

            # Determinar si es candidato a eliminación
            is_obsolete_candidate = any(obsolete_patterns.values())
            has_broken_refs = len(broken_refs) > 0
            is_unused = not usage_analysis['is_referenced']

            file_analysis = {
                'path': str(file_path.relative_to(self.project_root)),
                'absolute_path': str(file_path),
                'importance': importance,
                'obsolete_patterns': obsolete_patterns,
                'broken_references': broken_refs,
                'usage_analysis': usage_analysis,
                'is_obsolete_candidate': is_obsolete_candidate,
                'has_broken_refs': has_broken_refs,
                'is_unused': is_unused,
                'file_size': file_path.stat().st_size if file_path.exists() else 0
            }

            # Categorizar archivo
            if importance == 'CRITICAL':
                results['critical_files'].append(file_analysis)
            elif is_obsolete_candidate and (is_unused or importance in ['DEBUG', 'UTILITY']):
                results['safe_to_delete'].append(file_analysis)
            elif has_broken_refs or is_obsolete_candidate:
                results['requires_review'].append(file_analysis)

            if is_obsolete_candidate:
                results['obsolete_candidates'].append(file_analysis)

            if has_broken_refs:
                results['broken_references'].extend([
                    {
                        'file': str(file_path.relative_to(self.project_root)),
                        'broken_ref': ref
                    } for ref in broken_refs
                ])

        self.analysis_results = results
        return results

    def generate_cleanup_plan(self) -> Dict[str, List[str]]:
        """Genera plan de limpieza basado en el diagnóstico"""
        if not self.analysis_results:
            self.run_diagnostic()

        cleanup_plan = {
            'immediate_delete': [],
            'review_needed': [],
            'keep_files': []
        }

        for file_analysis in self.analysis_results['safe_to_delete']:
            cleanup_plan['immediate_delete'].append(file_analysis['path'])

        for file_analysis in self.analysis_results['requires_review']:
            cleanup_plan['review_needed'].append(file_analysis['path'])

        for file_analysis in self.analysis_results['critical_files']:
            cleanup_plan['keep_files'].append(file_analysis['path'])

        return cleanup_plan

    def save_diagnostic_report(self, output_path: Path = None):
        """Guarda reporte de diagnóstico en JSON"""
        if not self.analysis_results:
            self.run_diagnostic()

        if output_path is None:
            output_path = self.project_root / "docs" / "reports" / f"obsolete_files_diagnostic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, indent=2, ensure_ascii=False)

        enviar_senal_log("INFO", f"📊 Reporte guardado en: {output_path}", "obsolete_diagnostic", "save")
        return output_path

    def print_summary(self):
        """Imprime resumen del diagnóstico"""
        if not self.analysis_results:
            self.run_diagnostic()

        results = self.analysis_results

        enviar_senal_log("INFO", "=" * 60, "obsolete_diagnostic", "summary")
        enviar_senal_log("INFO", "📊 RESUMEN DE DIAGNÓSTICO DE ARCHIVOS OBSOLETOS", "obsolete_diagnostic", "summary")
        enviar_senal_log("INFO", "=" * 60, "obsolete_diagnostic", "summary")

        enviar_senal_log("INFO", f"📁 Total archivos analizados: {results['total_files']}", "obsolete_diagnostic", "summary")
        enviar_senal_log("INFO", f"🗑️ Candidatos obsoletos: {len(results['obsolete_candidates'])}", "obsolete_diagnostic", "summary")
        enviar_senal_log("INFO", f"🔗 Archivos con referencias rotas: {len(results['broken_references'])}", "obsolete_diagnostic", "summary")
        enviar_senal_log("INFO", f"✅ Archivos seguros para eliminar: {len(results['safe_to_delete'])}", "obsolete_diagnostic", "summary")
        enviar_senal_log("INFO", f"⚠️ Archivos que requieren revisión: {len(results['requires_review'])}", "obsolete_diagnostic", "summary")
        enviar_senal_log("INFO", f"🛡️ Archivos críticos protegidos: {len(results['critical_files'])}", "obsolete_diagnostic", "summary")

        # Mostrar archivos seguros para eliminar
        if results['safe_to_delete']:
            enviar_senal_log("INFO", "\n✅ ARCHIVOS SEGUROS PARA ELIMINAR:", "obsolete_diagnostic", "summary")
            for file_info in results['safe_to_delete'][:10]:  # Solo mostrar primeros 10
                enviar_senal_log("INFO", f"  - {file_info['path']}", "obsolete_diagnostic", "summary")

            if len(results['safe_to_delete']) > 10:
                enviar_senal_log("INFO", f"  ... y {len(results['safe_to_delete']) - 10} más", "obsolete_diagnostic", "summary")

        # Mostrar referencias rotas más comunes
        if results['broken_references']:
            enviar_senal_log("INFO", "\n🔗 REFERENCIAS ROTAS MÁS COMUNES:", "obsolete_diagnostic", "summary")
            broken_count = {}
            for ref in results['broken_references']:
                broken_ref = ref['broken_ref']
                broken_count[broken_ref] = broken_count.get(broken_ref, 0) + 1

            for ref, count in sorted(broken_count.items(), key=lambda x: x[1], reverse=True)[:5]:
                enviar_senal_log("INFO", f"  - {ref}: {count} archivos", "obsolete_diagnostic", "summary")

def main():
    """Función principal"""
    enviar_senal_log("INFO", "🔍 OBSOLETE FILES DIAGNOSTIC - ICT Engine v5.0", "obsolete_diagnostic", "main")
    enviar_senal_log("INFO", "📅 " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "obsolete_diagnostic", "main")
    enviar_senal_log("INFO", "=" * 60, "obsolete_diagnostic", "main")

    # Crear diagnosticador
    diagnostic = ObsoleteFilesDiagnostic()

    # Ejecutar diagnóstico
    results = diagnostic.run_diagnostic()

    # Mostrar resumen
    diagnostic.print_summary()

    # Guardar reporte
    report_path = diagnostic.save_diagnostic_report()

    # Generar plan de limpieza
    cleanup_plan = diagnostic.generate_cleanup_plan()

    enviar_senal_log("INFO", "\n🧹 PLAN DE LIMPIEZA GENERADO:", "obsolete_diagnostic", "main")
    enviar_senal_log("INFO", f"  - Eliminar inmediatamente: {len(cleanup_plan['immediate_delete'])} archivos", "obsolete_diagnostic", "main")
    enviar_senal_log("INFO", f"  - Revisar antes de eliminar: {len(cleanup_plan['review_needed'])} archivos", "obsolete_diagnostic", "main")
    enviar_senal_log("INFO", f"  - Mantener (críticos): {len(cleanup_plan['keep_files'])} archivos", "obsolete_diagnostic", "main")

    enviar_senal_log("INFO", f"\n📋 Reporte completo guardado en:", "obsolete_diagnostic", "main")
    enviar_senal_log("INFO", f"   {report_path}", "obsolete_diagnostic", "main")

    enviar_senal_log("INFO", "\n🎯 Para ejecutar limpieza automática:", "obsolete_diagnostic", "main")
    enviar_senal_log("INFO", "   python utilities/obsolete_files_diagnostic.py --cleanup", "obsolete_diagnostic", "main")

    return results

if __name__ == "__main__":
    # Verificar argumentos
    if len(sys.argv) > 1 and sys.argv[1] == "--cleanup":
        enviar_senal_log("INFO", "🧹 Ejecutando limpieza automática...", "obsolete_diagnostic", "cleanup")
        diagnostic = ObsoleteFilesDiagnostic()
        results = diagnostic.run_diagnostic()
        cleanup_plan = diagnostic.generate_cleanup_plan()

        # Eliminar archivos seguros
        deleted_count = 0
        for file_path in cleanup_plan['immediate_delete']:
            full_path = PROJECT_ROOT / file_path
            try:
                if full_path.exists():
                    full_path.unlink()
                    enviar_senal_log("INFO", f"✅ Eliminado: {file_path}", "obsolete_diagnostic", "cleanup")
                    deleted_count += 1
                else:
                    enviar_senal_log("WARNING", f"⚠️ No encontrado: {file_path}", "obsolete_diagnostic", "cleanup")
            except Exception as e:
                enviar_senal_log("ERROR", f"❌ Error eliminando {file_path}: {e}", "obsolete_diagnostic", "cleanup")

        enviar_senal_log("INFO", f"🎉 Limpieza completada: {deleted_count} archivos eliminados", "obsolete_diagnostic", "cleanup")
    else:
        main()
