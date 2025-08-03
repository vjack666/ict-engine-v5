from sistema.logging_interface import enviar_senal_log
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
=============================================================================
SCRIPT DE LIMPIEZA SEGURA - ICT ENGINE v5.0
=============================================================================

Ejecuta limpieza por fases de archivos no utilizados basado en el análisis
generado por unused_files_analyzer.py

FASES DE LIMPIEZA:
1. FASE 1: Archivos de cache (.pyc, __pycache__) - COMPLETAMENTE SEGURO
2. FASE 2: Scripts de fix ya ejecutados - REVISAR ANTES
3. FASE 3: Archivos de backup (.bak) - VERIFICAR ORIGINALS
4. FASE 4: Logs antiguos - MANTENER RECIENTES
5. FASE 5: Archivos duplicados - COMPARAR CONTENIDO
"""

import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Union, Optional, Any
import sys

class SafeFileCleanup:
    """
    Limpieza segura de archivos por fases
    """

    def __init__(self):
        self.base_path = Path(r"c:\Users\v_jac\Desktop\itc engine v5.0")
        self.backup_path = self.base_path / "temp" / "cleanup_backup"
        self.deleted_files = []
        self.skipped_files = []

        # Crear carpeta de backup
        self.backup_path.mkdir(parents=True, exist_ok=True)

    def fase_1_cache_cleanup(self) -> Dict[str, Union[int, List[str]]]:
        """FASE 1: Limpieza de archivos de cache - COMPLETAMENTE SEGURO"""
        enviar_senal_log("INFO", "🧹 FASE 1: Limpiando archivos de cache...", "safe_file_cleanup", "migration")
        enviar_senal_log("INFO", "=" * 50, "safe_file_cleanup", "migration")

        deleted = []

        # Eliminar todos los archivos .pyc y directorios __pycache__
        for pycache_dir in self.base_path.rglob("__pycache__"):
            if pycache_dir.is_dir():
                try:
                    shutil.rmtree(pycache_dir)
                    deleted.append(str(pycache_dir.relative_to(self.base_path)))
                    enviar_senal_log("INFO", f"✅ Eliminado: {pycache_dir.relative_to(self.base_path, "safe_file_cleanup", "migration")}")
                except Exception as e:
                    enviar_senal_log("ERROR", f"❌ Error eliminando {pycache_dir}: {e}", "safe_file_cleanup", "migration")

        # Eliminar archivos .pyc sueltos
        for pyc_file in self.base_path.rglob("*.pyc"):
            try:
                pyc_file.unlink()
                deleted.append(str(pyc_file.relative_to(self.base_path)))
                enviar_senal_log("INFO", f"✅ Eliminado: {pyc_file.relative_to(self.base_path, "safe_file_cleanup", "migration")}")
            except Exception as e:
                enviar_senal_log("ERROR", f"❌ Error eliminando {pyc_file}: {e}", "safe_file_cleanup", "migration")

        enviar_senal_log("INFO", f"\\n🎯 FASE 1 COMPLETADA: {len(deleted, "safe_file_cleanup", "migration")} elementos eliminados")
        return {"deleted": len(deleted), "files": deleted}

    def fase_2_fix_scripts_review(self) -> Dict[str, List[str]]:
        """FASE 2: Revisar scripts de fix - REQUIERE CONFIRMACIÓN"""
        enviar_senal_log("INFO", "\\n🔧 FASE 2: Revisando scripts de fix...", "safe_file_cleanup", "migration")
        enviar_senal_log("INFO", "=" * 50, "safe_file_cleanup", "migration")

        fix_scripts = [
            "debugging/fix_logging_emoji_errors.py",
            "debugging/tct_instant_fix.py",
            "debugging/tct_live_hotfix.py",
            "debugging/tct_quick_fix.py",
            "scripts/fix_acc_flow_controller.py",
            "scripts/fix_escaped_quotes.py",
            "scripts/fix_jsondecode_critical.py",
            "scripts/fix_jsondecode_error.py",
            "scripts/fix_log_encoding.py",
            "scripts/fix_tct_logging_params.py",
            "scripts/fix_tct_pipeline_logging.py",
            "scripts/quick_fixes.py"
        ]

        recommendations = {
            "safe_to_delete": [],
            "keep_for_reference": [],
            "review_needed": []
        }

        for script_path in fix_scripts:
            full_path = self.base_path / script_path
            if full_path.exists():
                # Analizar si el script es reutilizable
                if self._is_reusable_fix_script(full_path):
                    recommendations["keep_for_reference"].append(script_path)
                    enviar_senal_log("INFO", f"📚 MANTENER: {script_path} (reutilizable, "safe_file_cleanup", "migration")")
                elif self._is_one_time_fix(full_path):
                    recommendations["safe_to_delete"].append(script_path)
                    enviar_senal_log("INFO", f"🗑️ SEGURO BORRAR: {script_path} (fix de una vez, "safe_file_cleanup", "migration")")
                else:
                    recommendations["review_needed"].append(script_path)
                    enviar_senal_log("INFO", f"⚠️ REVISAR: {script_path} (requiere análisis, "safe_file_cleanup", "migration")")

        return recommendations

    def fase_3_backup_files_cleanup(self) -> Dict[str, int]:
        """FASE 3: Limpieza de archivos de backup - VERIFICAR ORIGINALES"""
        enviar_senal_log("INFO", "\\n🗂️ FASE 3: Procesando archivos de backup...", "safe_file_cleanup", "migration")
        enviar_senal_log("INFO", "=" * 50, "safe_file_cleanup", "migration")

        backup_files = [
            "core/analysis_command_center/acc_data_models.py.bak",
            "core/analysis_command_center/acc_flow_controller.py.bak",
            "core/analysis_command_center/acc_orchestrator.py.bak",
            "core/trading.py.bak",
            "scripts/master_sluc_v21_updater.py.bak",
            "sistema/logging_interface_v20_backup.py",
            "sistema/logging_interface_v20_backup.py.bak"
        ]

        safe_to_delete = []
        needs_review = []

        for backup_path in backup_files:
            full_backup_path = self.base_path / backup_path
            if full_backup_path.exists():
                # Verificar si existe el archivo original
                original_path = self._get_original_path(full_backup_path)
                if original_path and original_path.exists():
                    # Verificar que el original funcione
                    if self._verify_original_works(original_path):
                        safe_to_delete.append(backup_path)
                        enviar_senal_log("INFO", f"✅ SEGURO BORRAR: {backup_path} (original funciona, "safe_file_cleanup", "migration")")
                    else:
                        needs_review.append(backup_path)
                        enviar_senal_log("INFO", f"⚠️ MANTENER: {backup_path} (original problemático, "safe_file_cleanup", "migration")")
                else:
                    needs_review.append(backup_path)
                    enviar_senal_log("INFO", f"⚠️ MANTENER: {backup_path} (no existe original, "safe_file_cleanup", "migration")")

        return {"safe_to_delete": len(safe_to_delete), "needs_review": len(needs_review)}

    def fase_4_log_cleanup(self) -> Dict[str, int]:
        """FASE 4: Limpieza de logs antiguos - MANTENER RECIENTES"""
        enviar_senal_log("INFO", "\\n📋 FASE 4: Limpiando logs antiguos...", "safe_file_cleanup", "migration")
        enviar_senal_log("INFO", "=" * 50, "safe_file_cleanup", "migration")

        # Mantener logs de los últimos 3 días
        cutoff_date = datetime.now() - timedelta(days=3)

        old_logs = []
        recent_logs = []

        for log_file in self.base_path.rglob("*.log"):
            try:
                file_date = datetime.fromtimestamp(log_file.stat().st_mtime)
                if file_date < cutoff_date:
                    old_logs.append(str(log_file.relative_to(self.base_path)))
                    enviar_senal_log("INFO", f"🗑️ LOG ANTIGUO: {log_file.relative_to(self.base_path, "safe_file_cleanup", "migration")}")
                else:
                    recent_logs.append(str(log_file.relative_to(self.base_path)))
                    enviar_senal_log("INFO", f"📚 LOG RECIENTE: {log_file.relative_to(self.base_path, "safe_file_cleanup", "migration")}")
            except Exception as e:
                enviar_senal_log("ERROR", f"❌ Error procesando {log_file}: {e}", "safe_file_cleanup", "migration")

        return {"old_logs": len(old_logs), "recent_logs": len(recent_logs)}

    def _is_reusable_fix_script(self, script_path: Path) -> bool:
        """Determina si un script de fix es reutilizable"""
        try:
            content = script_path.read_text(encoding='utf-8')
            # Scripts que contienen funciones genéricas son reutilizables
            reusable_indicators = [
                'def fix_', 'class Fix', 'def repair_', 'def update_all',
                'master_', 'batch_', 'auto_repair'
            ]
            return any(indicator in content for indicator in reusable_indicators)
        except:
            return False

    def _is_one_time_fix(self, script_path: Path) -> bool:
        """Determina si un script de fix es de una sola vez"""
        try:
            content = script_path.read_text(encoding='utf-8')
            one_time_indicators = [
                'instant_fix', 'quick_fix', 'hotfix', 'emergency',
                'specific_fix', 'one_time'
            ]
            return any(indicator in content for indicator in one_time_indicators)
        except:
            return False

    def _get_original_path(self, backup_path: Path) -> Optional[Path]:
        """Obtiene la ruta del archivo original"""
        if backup_path.name.endswith('.bak'):
            return backup_path.with_suffix('')
        elif '_backup' in backup_path.name:
            original_name = backup_path.name.replace('_backup', '').replace('_v20', '')
            return backup_path.with_name(original_name)
        return None

    def _verify_original_works(self, original_path: Path) -> bool:
        """Verifica que el archivo original funcione (verificación básica)"""
        try:
            if original_path.suffix == '.py':
                # Para archivos Python, verificar sintaxis básica
                content = original_path.read_text(encoding='utf-8')
                compile(content, str(original_path), 'exec')
                return True
            else:
                # Para otros archivos, verificar que se puedan leer
                original_path.read_text(encoding='utf-8')
                return True
        except:
            return False

    def execute_safe_cleanup(self) -> Dict[str, Any]:
        """Ejecuta limpieza segura completa"""
        enviar_senal_log("INFO", "🗑️ LIMPIEZA SEGURA ICT ENGINE v5.0", "safe_file_cleanup", "migration")
        enviar_senal_log("INFO", "=" * 60, "safe_file_cleanup", "migration")
        enviar_senal_log("INFO", f"📁 Workspace: {self.base_path}", "safe_file_cleanup", "migration")
        enviar_senal_log("INFO", f"🔒 Backup: {self.backup_path}", "safe_file_cleanup", "migration")
        enviar_senal_log("INFO", "", "safe_file_cleanup", "migration")

        results = {}

        # FASE 1: Cache (automático)
        results['fase_1_cache'] = self.fase_1_cache_cleanup()

        # FASE 2: Scripts de fix (revisar)
        results['fase_2_fix_scripts'] = self.fase_2_fix_scripts_review()

        # FASE 3: Backups (verificar)
        results['fase_3_backups'] = self.fase_3_backup_files_cleanup()

        # FASE 4: Logs (mantener recientes)
        results['fase_4_logs'] = self.fase_4_log_cleanup()

        return results

    def generate_cleanup_report(self, results: Dict) -> str:
        """Genera reporte de limpieza"""
        report = []
        report.append("# 🗑️ REPORTE DE LIMPIEZA SEGURA")
        report.append("")
        report.append(f"**Fecha:** {datetime.now().strftime('%d de %B de %Y')}")
        report.append(f"**Workspace:** ICT Engine v5.0")
        report.append("**Estado:** ✅ ANÁLISIS COMPLETADO")
        report.append("")
        report.append("---")
        report.append("")

        # Resumen por fases
        for fase, data in results.items():
            report.append(f"## {fase.replace('_', ' ').title()}")
            report.append("")
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        report.append(f"**{key}:** {len(value)} archivos")
                        if value:  # Solo mostrar si hay elementos
                            report.append("```")
                            for item in value[:10]:  # Limitar a 10 elementos
                                report.append(item)
                            if len(value) > 10:
                                report.append(f"... y {len(value) - 10} más")
                            report.append("```")
                    else:
                        report.append(f"**{key}:** {value}")
            report.append("")

        report.append("---")
        report.append("**Generado por:** SafeFileCleanup v1.0")

        return "\\n".join(report)

def main():
    """Función principal"""
    cleanup = SafeFileCleanup()

    enviar_senal_log("INFO", "🚀 Iniciando análisis de limpieza segura...", "safe_file_cleanup", "migration")
    results = cleanup.execute_safe_cleanup()

    # Generar reporte
    report = cleanup.generate_cleanup_report(results)

    # Guardar reporte
    report_path = Path("docs/bitacoras/reportes/LIMPIEZA_SEGURA_REPORTE.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    enviar_senal_log("INFO", f"\\n📄 Reporte guardado: {report_path}", "safe_file_cleanup", "migration")
    enviar_senal_log("INFO", "✅ Análisis de limpieza completado", "safe_file_cleanup", "migration")

if __name__ == "__main__":
    main()
