#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
=============================================================================
MASTER SCRIPT - ACTUALIZACIÓN COMPLETA SLUC v2.1
=============================================================================

Script maestro para actualizar TODOS los archivos del sistema con:
- Parámetros correctos de enviar_senal_log
- Compatibilidad total con SLUC v2.1
- Routing inteligente automático
- Funciones específicas por módulo

Objetivo: Migración completa del sistema a SLUC v2.1
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

class SLUCv21MasterUpdater:
    """
    Actualizador maestro para migración completa a SLUC v2.1
    """

    def __init__(self):
        self.base_path = Path(r"c:\Users\v_jac\Desktop\itc engine v5.0")
        self.files_processed = 0
        self.files_updated = 0
        self.errors = []

        # Archivos a excluir (backups y archivos especiales)
        self.exclude_patterns = [
            '*_backup.py',
            '*_v20_backup.py',
            '__pycache__',
            '*.pyc',
            'scripts/fix_*.py',  # Scripts de fix
            'sistema/logging_interface_v21.py'  # Ya está correcto
        ]

        # Patrones de reemplazo para parámetros incorrectos
        self.replacements = [
            # Parámetros con nombres incorrectos
            (r"nivel='([^']*)'", r"nivel='\1'"),
            (r'nivel="([^"]*)"', r'nivel="\1"'),
            (r"mensaje='([^']*)'", r"mensaje='\1'"),
            (r'mensaje="([^"]*)"', r'mensaje="\1"'),
            (r"fuente='([^']*)'", r"fuente='\1'"),
            (r'fuente="([^"]*)"', r'fuente="\1"'),

            # Casos específicos de líneas múltiples
            (r"message=f\"([^\"]*)\",", r"mensaje=f\"\1\","),
            (r"message=f'([^']*)',", r"mensaje=f'\1',"),
            (r"fuente=__name__,", r"fuente=__name__,"),
            (r"fuente='([^']*)',", r"fuente='\1',"),
            (r'fuente="([^"]*)",', r'fuente="\1",'),
        ]

        # Archivos prioritarios para actualizar primero
        self.priority_files = [
            'core/trading.py',
            'core/limit_order_manager.py',
            'core/ict_engine/ict_detector.py',
            'core/analysis_command_center/acc_orchestrator.py',
            'utils/mt5_data_manager.py',
            'dashboard/dashboard_controller.py',
            'dashboard/dashboard_widgets.py'
        ]

    def should_exclude_file(self, file_path: Path) -> bool:
        """Verifica si un archivo debe ser excluido"""
        file_str = str(file_path)

        for pattern in self.exclude_patterns:
            if pattern in file_str or file_path.name.startswith('fix_'):
                return True

        return False

    def find_python_files_with_logging(self) -> List[Path]:
        """Encuentra todos los archivos Python que usan enviar_senal_log"""
        files = []

        for py_file in self.base_path.rglob("*.py"):
            if self.should_exclude_file(py_file):
                continue

            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'enviar_senal_log(' in content:
                        files.append(py_file)
            except Exception as e:
                self.errors.append(f"Error leyendo {py_file}: {e}")

        return files

    def update_file_logging(self, file_path: Path) -> Tuple[bool, str]:
        """
        Actualiza un archivo específico con los parámetros correctos
        Retorna: (was_updated, message)
        """
        try:
            # Leer archivo
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            # Aplicar reemplazos
            updated_content = original_content
            changes_made = []

            for old_pattern, new_pattern in self.replacements:
                matches_before = len(re.findall(old_pattern, updated_content))
                updated_content = re.sub(old_pattern, new_pattern, updated_content)
                matches_after = len(re.findall(old_pattern, updated_content))

                if matches_before > matches_after:
                    changes_made.append(f"{old_pattern} -> {new_pattern} ({matches_before - matches_after} cambios)")

            # Verificar si hubo cambios
            if updated_content != original_content:
                # Crear backup
                backup_path = file_path.with_suffix('.py.bak')
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)

                # Escribir archivo actualizado
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)

                return True, f"Actualizado: {', '.join(changes_made)}"
            else:
                return False, "Sin cambios necesarios"

        except Exception as e:
            return False, f"Error: {e}"

    def update_imports(self, file_path: Path) -> bool:
        """Actualiza los imports para usar las funciones específicas por módulo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Detectar tipo de módulo basado en la ruta
            file_str = str(file_path).lower()
            module_type = None

            if 'trading' in file_str:
                module_type = 'trading'
            elif 'ict' in file_str:
                module_type = 'ict'
            elif 'poi' in file_str:
                module_type = 'poi'
            elif 'mt5' in file_str:
                module_type = 'mt5'
            elif 'dashboard' in file_str:
                module_type = 'dashboard'
            elif 'tct' in file_str:
                module_type = 'tct'
            elif 'metrics' in file_str or 'metric' in file_str:
                module_type = 'metrics'

            # Agregar import específico si corresponde
            if module_type and f'log_{module_type}' not in content:
                # Buscar línea de import existente
                import_pattern = r'from sistema\.logging_interface import enviar_senal_log'
                if re.search(import_pattern, content):
                    new_import = f'from sistema.logging_interface import enviar_senal_log, log_{module_type}'
                    content = re.sub(import_pattern, new_import, content)

                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    return True

            return False

        except Exception as e:
            self.errors.append(f"Error actualizando imports en {file_path}: {e}")
            return False

    def run_complete_update(self):
        """Ejecuta la actualización completa del sistema"""
        enviar_senal_log("INFO", "🔄 INICIANDO ACTUALIZACIÓN COMPLETA A SLUC v2.1", "master_sluc_v21_updater", "migration")
        enviar_senal_log("INFO", "=" * 60, "master_sluc_v21_updater", "migration")

        # Encontrar archivos
        enviar_senal_log("INFO", "📁 Buscando archivos Python con logging...", "master_sluc_v21_updater", "migration")
        files = self.find_python_files_with_logging()
        enviar_senal_log("INFO", f"   Encontrados: {len(files, "master_sluc_v21_updater", "migration")} archivos")

        # Ordenar archivos por prioridad
        priority_files = []
        regular_files = []

        for file_path in files:
            relative_path = str(file_path.relative_to(self.base_path))
            if any(priority in relative_path for priority in self.priority_files):
                priority_files.append(file_path)
            else:
                regular_files.append(file_path)

        all_files = priority_files + regular_files

        enviar_senal_log("INFO", f"📋 Archivos prioritarios: {len(priority_files, "master_sluc_v21_updater", "migration")}")
        enviar_senal_log("INFO", f"📋 Archivos regulares: {len(regular_files, "master_sluc_v21_updater", "migration")}")
        enviar_senal_log("INFO", , "master_sluc_v21_updater", "migration")

        # Procesar archivos
        for i, file_path in enumerate(all_files, 1):
            relative_path = file_path.relative_to(self.base_path)
            enviar_senal_log("INFO", f"[{i:3d}/{len(all_files, "master_sluc_v21_updater", "migration")}] Procesando: {relative_path}")

            self.files_processed += 1

            # Actualizar parámetros de logging
            was_updated, message = self.update_file_logging(file_path)
            if was_updated:
                self.files_updated += 1
                enviar_senal_log("INFO", f"   ✅ {message}", "master_sluc_v21_updater", "migration")
            else:
                enviar_senal_log("INFO", f"   📝 {message}", "master_sluc_v21_updater", "migration")

            # Actualizar imports
            imports_updated = self.update_imports(file_path)
            if imports_updated:
                enviar_senal_log("INFO", f"   📦 Imports actualizados", "master_sluc_v21_updater", "migration")

        enviar_senal_log("INFO", , "master_sluc_v21_updater", "migration")
        enviar_senal_log("INFO", "=" * 60, "master_sluc_v21_updater", "migration")
        enviar_senal_log("INFO", "✅ ACTUALIZACIÓN COMPLETA FINALIZADA", "master_sluc_v21_updater", "migration")
        enviar_senal_log("INFO", f"📊 Archivos procesados: {self.files_processed}", "master_sluc_v21_updater", "migration")
        enviar_senal_log("INFO", f"📊 Archivos actualizados: {self.files_updated}", "master_sluc_v21_updater", "migration")
        enviar_senal_log("ERROR", f"📊 Errores: {len(self.errors, "master_sluc_v21_updater", "migration")}")

        if self.errors:
            enviar_senal_log("INFO", , "master_sluc_v21_updater", "migration")
            enviar_senal_log("ERROR", "❌ Errores encontrados:", "master_sluc_v21_updater", "migration")
            for error in self.errors[:10]:  # Mostrar solo los primeros 10
                enviar_senal_log("ERROR", f"   - {error}", "master_sluc_v21_updater", "migration")
            if len(self.errors) > 10:
                enviar_senal_log("ERROR", f"   ... y {len(self.errors, "master_sluc_v21_updater", "migration") - 10} errores más")

        enviar_senal_log("INFO", , "master_sluc_v21_updater", "migration")
        enviar_senal_log("INFO", "🎯 PRÓXIMOS PASOS:", "master_sluc_v21_updater", "migration")
        enviar_senal_log("ERROR", "   1. Verificar que no hay errores de sintaxis", "master_sluc_v21_updater", "migration")
        enviar_senal_log("INFO", "   2. Probar el dashboard", "master_sluc_v21_updater", "migration")
        enviar_senal_log("INFO", "   3. Validar routing de logs", "master_sluc_v21_updater", "migration")
        enviar_senal_log("INFO", "   4. Confirmar compatibilidad total", "master_sluc_v21_updater", "migration")

def main():
    """Función principal"""
    updater = SLUCv21MasterUpdater()
    updater.run_complete_update()

if __name__ == "__main__":
    main()
