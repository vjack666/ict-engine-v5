#!/usr/bin/env python3
"""
🧹 FASE 2 CLEANUP - Archivos con referencias rotas
================================================

Limpieza de archivos que tienen referencias a módulos obsoletos eliminados.
"""

import os
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent

def log_message(level: str, message: str):
    """Log message simple"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")

def fase_2_cleanup():
    """Ejecuta limpieza FASE 2 de archivos con referencias rotas"""

    # Archivos identificados con referencias rotas que no son críticos
    obsolete_files = [
        # Archivos de debugging/testing
        "debugging/diagnose_poi_system.py",
        "debugging/diagnose_tct_pipeline.py",
        "debugging/verify_fvg_fix.py",
        "debugging/verify_sluc_names_fix.py",

        # Archivos de migración temporal
        "utilities/migration/simple_print_migration.py",

        # Scripts de sprint ejecutor obsoleto
        "utilities/sprint/sprint_1_2_refactored_executor.py",

        # Widgets con referencias rotas (no utilizados en dashboard principal)
        "dashboard/simple_candle_widget.py",
        "dashboard/widgets/ict_analytics_widget.py",

        # Integraciones obsoletas
        "core/integrations/analytics_integration.py",
        "core/data_management/candle_coordinator.py",

        # Scripts de diagnóstico obsoletos
        "utilities/obsolete_files_diagnostic.py"
    ]

    log_message("INFO", "🧹 FASE 2 CLEANUP - Eliminando archivos con referencias rotas")
    log_message("INFO", f"📋 {len(obsolete_files)} archivos programados para eliminación")

    deleted_count = 0
    error_count = 0

    for file_path in obsolete_files:
        full_path = PROJECT_ROOT / file_path

        try:
            if full_path.exists():
                # Verificar que no sea un archivo crítico
                if any(critical in file_path for critical in ['main.py', 'mt5_data_manager.py', 'dashboard_definitivo.py']):
                    log_message("WARNING", f"⚠️ Saltando archivo crítico: {file_path}")
                    continue

                full_path.unlink()
                log_message("INFO", f"✅ Eliminado: {file_path}")
                deleted_count += 1
            else:
                log_message("WARNING", f"⚠️ No encontrado: {file_path}")

        except Exception as e:
            log_message("ERROR", f"❌ Error eliminando {file_path}: {e}")
            error_count += 1

    log_message("INFO", f"🎉 FASE 2 completada:")
    log_message("INFO", f"  ✅ Eliminados: {deleted_count} archivos")
    log_message("INFO", f"  ❌ Errores: {error_count} archivos")

    return deleted_count, error_count

def main():
    """Función principal"""
    log_message("INFO", "🧹 FASE 2 CLEANUP - ICT Engine v5.0")
    log_message("INFO", f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_message("INFO", "=" * 60)

    # Ejecutar limpieza
    deleted, errors = fase_2_cleanup()

    log_message("INFO", "=" * 60)
    log_message("INFO", "✨ FASE 2 CLEANUP COMPLETADA")

    if deleted > 0:
        log_message("INFO", f"🗑️ Se eliminaron {deleted} archivos obsoletos")
        log_message("INFO", "🔄 Recomendación: Ejecutar pruebas de funcionamiento")
        log_message("INFO", "   python main.py")
        log_message("INFO", "   python dashboard/dashboard_definitivo.py")

    if errors > 0:
        log_message("WARNING", f"⚠️ {errors} archivos no pudieron ser eliminados")

if __name__ == "__main__":
    main()
